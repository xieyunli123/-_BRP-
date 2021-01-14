import os

import pandas as pd
import tensorflow as tf

cur_dir = os.path.dirname(os.path.abspath(__file__))
# base_dir = os.path.dirname(os.path.dirname(os.path.dirname(cur_dir)))
data_dir = os.path.join(cur_dir, "data")

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

_CSV_COLUMNS = [
    "user_id", "poem_id", "age", "gender", "device_id",
    "weather_tag", "wind_tag", "temperature_tag", "time_tag", "season_tag", "festival_tag", "region_tag",
    "star"
]  # 原始数据CSV文件，列名

_CSV_COLUMN_DEFAULTS = [[0], [0], [0], [0], [""],
                        [''], [''], [''], [''], [''], [''], ['']]  # CSV文件每列默认值


def read_data(data_file, test=False):
    """生成训练数据"""
    tf_data = pd.read_csv(
        tf.gfile.Open(data_file),
        names=_CSV_COLUMNS,
        skip_blank_lines=True, skipinitialspace=True,
        engine="python",
        skiprows=1
    )
    tf_data = tf_data.dropna(how="any", axis=1)  # remove Na elements
    n_classes = 10  # 默认2
    labels = tf_data["star"].apply(lambda x: max(int(x), n_classes - 1)).astype(int)
    return tf_data, labels


def input_fn(data_file, num_epochs, shuffle, batch_size):
    tf_data, labels = read_data(data_file)
    return tf.estimator.inputs.pandas_input_fn(
        x=tf_data,
        y=labels,
        batch_size=batch_size,
        num_epochs=num_epochs,
        shuffle=shuffle,
        num_threads=1
    )


def get_feature_column():
    """
    连续值放入deep侧，离散值放入wide侧；
    具体处理：
    连续值离散化后放入wide侧
    离散值：
    hash，然后embeeding，放入wide侧
    user_id,poem_id,
    age,gender,device_id,
    weather_tag,wind_tag,temperature_tag,time_tag,season_tag,festival_tag,region_tag,
    star
    :return:
    """
    # 连续值处理
    user_id = tf.feature_column.categorical_column_with_vocabulary_list(
        "user_id", list(range(1, 10001)))
    poem_id = tf.feature_column.categorical_column_with_vocabulary_list(
        "poem_id", list(range(0, 76557 + 1)))
    age = tf.feature_column.numeric_column("age")
    gender = tf.feature_column.categorical_column_with_vocabulary_list(
        "gender", ["男", "女"])
    device_id = tf.feature_column.categorical_column_with_vocabulary_list(
        "device_id", ["Android", "iPhone"])
    weather_tag = tf.feature_column.categorical_column_with_vocabulary_list(
        "weather_tag", ['晴', '雨', '小雨', '大雨', '阴', '云', '雪', '雷电', '干旱', '沙尘', '雾'])
    wind_tag = tf.feature_column.categorical_column_with_vocabulary_list(
        "wind_tag", ['风', '无风', '东风', '南风', '西风', '北风', '微风', '大风'])
    temperature_tag = tf.feature_column.categorical_column_with_vocabulary_list(
        "temperature_tag", ['寒冷', '炎热', "未知"])
    time_tag = tf.feature_column.categorical_column_with_vocabulary_list(
        "time_tag", ['日出', '日落', '正午', '上午', '下午', '晚上', '凌晨'])
    season_tag = tf.feature_column.categorical_column_with_vocabulary_list(
        "season_tag", ['春', '夏', '秋', '冬'])
    festival_tag = tf.feature_column.categorical_column_with_vocabulary_list(
        "festival_tag", ['除夕', '春节', '新年', '元宵', '寒食', '清明', '端午', '七夕', '爱情', '中秋', '重阳', '劳动', '爱国',
                         '妇女', '母亲', '父亲', '儿童', '老师', "无"])
    region_tag = tf.feature_column.categorical_column_with_vocabulary_list(
        "region_tag", ['华东', '华南', '华中', '华北', '西北', '西南', '江南', '边塞', '西域', '徽州', '长安', '武陵',
                       '浔阳', '姑苏', '苏州', '扬州', '燕京', '庐州', '琅琊', '石头城', '景德镇', '京口', '临安', '广陵',
                       '钱塘', '金陵', '幽州', '洛阳', '凉州', '齐州', '蜀地', '汝南', '大梁', '泰山', '华山', '衡山', '恒山',
                       '嵩山', '黄山', '庐山', '雁荡山', '长江', '黄河', '黄鹤楼', '滕王阁', '岳阳楼', '玉门', '阳关', '瓜州',
                       '锦城', '成都', '洞庭', '西湖', '赤壁', '荒漠', '草原', '雪山'])
    # 连续值离散化
    age_bucket = tf.feature_column.bucketized_column(age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60])
    # 交叉特征
    cross_columns = [
        tf.feature_column.crossed_column([age_bucket, festival_tag], hash_bucket_size=300),
        tf.feature_column.crossed_column([age_bucket, gender, festival_tag], hash_bucket_size=16),
    ]

    # 特征
    base_columns = [user_id, poem_id, age, gender, device_id,
                    weather_tag, wind_tag, temperature_tag, time_tag, season_tag, festival_tag, region_tag]
    wide_columns = base_columns + cross_columns
    deep_columns = [
        # 连续值
        age,
        # 离散值的 embedding
        tf.feature_column.embedding_column(weather_tag, 9),
        tf.feature_column.embedding_column(wind_tag, 9),
        tf.feature_column.embedding_column(temperature_tag, 9),
        tf.feature_column.embedding_column(time_tag, 9),
        tf.feature_column.embedding_column(season_tag, 9),
        tf.feature_column.embedding_column(festival_tag, 9),
        tf.feature_column.embedding_column(region_tag, 9),
    ]
    return wide_columns, deep_columns
