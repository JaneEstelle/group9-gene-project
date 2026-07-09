# 导入csv标准库，用于将生成的序列、突变、距离数据写入csv文件持久保存
import csv
# 导入random标准库，提供随机数、随机采样、随机选择功能，生成仿真生物数据
import random
# 导入os标准库，用于文件路径拼接、文件夹自动创建等文件系统操作
import os


def _ensure_dir(file_path):
    """工具函数：自动创建文件所在目录，消除多处重复创建文件夹代码"""
    # 获取传入文件路径对应的父文件夹路径
    folder = os.path.dirname(file_path)
    # 判断文件夹路径非空时创建目录，exist_ok=True目录已存在不会报错
    if folder:
        os.makedirs(folder, exist_ok=True)


def _write_csv(file_path, data_list, headers):
    """通用CSV写入工具，复用序列/突变/距离三处重复的csv写入逻辑"""
    # 调用工具函数，自动生成文件存放文件夹
    _ensure_dir(file_path)
    # with上下文打开文件，程序结束自动关闭文件，newline消除windows多余空行，utf-8统一编码
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        # 创建字典写入器，指定csv表头字段
        writer = csv.DictWriter(f, fieldnames=headers)
        # 在csv第一行写入表头
        writer.writeheader()
        # 批量一次性写入所有数据字典，替代单行循环写入
        writer.writerows(data_list)


def generate_random_dna_sequence(length):
    """生成指定长度随机DNA串，碱基仅包含 A/T/G/C"""
    # 定义DNA四种标准碱基列表
    bases = ["A", "T", "G", "C"]
    # 随机选取length个碱基拼接为完整DNA字符串并返回
    return "".join(random.choices(bases, k=length))


def _mutate_base(origin):
    """生成和原碱基不同的新碱基，简化突变替换重复判断逻辑"""
    # 定义DNA四种标准碱基列表
    bases = ["A", "T", "G", "C"]
    # 过滤掉原始碱基，生成可选突变碱基列表
    candidates = [b for b in bases if b != origin]
    # 从可选碱基中随机选一个作为突变后的碱基返回
    return random.choice(candidates)


def generate_sequences(output_file=None):
    # 定义5种灵长类参考物种池，程序从中随机挑选使用
    species_pool = ["Homo sapiens", "Pan troglodytes", "Gorilla gorilla", "Pongo abelii", "Macaca mulatta"]
    # 随机选取3~5个不同物种作为本次数据集的使用物种
    used_species = random.sample(species_pool, k=random.randint(3, 5))
    # 空列表，存储全部生成完成的序列字典数据
    all_seqs = []
    # 固定总生成序列数量为10条
    total = 10

    # 遍历选中的物种，sp_idx为当前物种下标，sp_name为物种名称
    for sp_idx, sp_name in enumerate(used_species):
        # 随机生成该物种原始基准序列长度，区间20~100
        base_len = random.randint(20, 100)
        # 调用函数生成该物种无突变的原始基准DNA序列
        base_dna = generate_random_dna_sequence(base_len)
        # 计算每个物种平均分配到的序列基础数量
        sp_seq_count = total // len(used_species)
        # 余数分配，前若干物种多分配1条，保证总序列严格等于10
        if sp_idx < total % len(used_species):
            sp_seq_count += 1

        # 循环生成当前物种下所有分配数量的序列，seq_idx为物种内序列下标
        for seq_idx in range(sp_seq_count):
            # f-string格式化生成两位数字序列唯一ID，格式 seq_物种编号_序列编号
            sid = f"seq_{sp_idx+1:02}_{seq_idx+1:02}"
            # 物种第一条序列直接使用原始基准序列，不做突变
            if seq_idx == 0:
                dna_str = base_dna
            # 同物种其余序列，在基准序列上添加随机突变
            else:
                # 随机1~3个突变位点
                mut_cnt = random.randint(1, 3)
                # 将基准DNA字符串转为列表，支持单碱基修改操作
                dna_list = list(base_dna)
                # 循环执行对应次数碱基替换突变
                for _ in range(mut_cnt):
                    # 随机选取一个碱基位置下标
                    pos = random.randint(0, len(dna_list)-1)
                    # 调用工具函数替换该位置碱基，保证突变前后碱基不同
                    dna_list[pos] = _mutate_base(dna_list[pos])
                # 将修改后的碱基列表还原为完整DNA字符串
                dna_str = "".join(dna_list)
            # 将当前序列信息封装为字典，存入总序列列表
            all_seqs.append({
                "sequence_id": sid,
                "species_name": sp_name,
                "sequence_type": "DNA",
                "sequence_string": dna_str
            })
    # 如果传入了输出文件路径，调用通用工具写入csv文件
    if output_file:
        _write_csv(output_file, all_seqs, ["sequence_id", "species_name", "sequence_type", "sequence_string"])
    # 返回全部序列数据列表，供突变生成函数调用
    return all_seqs


def generate_mutations(sequences, output_file=None):
    # 空列表，存储所有生成完成的突变记录字典
    all_muts = []
    # 遍历每一条已生成的DNA序列
    for seq in sequences:
        # 获取当前序列唯一ID，用于突变数据关联
        sid = seq["sequence_id"]
        # 获取当前序列完整DNA碱基字符串
        dna = seq["sequence_string"]
        # 随机3~5个突变位点，上限不超过序列总长度的一半，避免过度突变
        max_mut = min(random.randint(3, 5), len(dna) // 2)
        # 使用集合存储已使用突变位置，自动去重，防止同一位点多次突变
        used_pos = set()
        # 循环生成对应数量的突变记录
        for _ in range(max_mut):
            # 随机选取一个碱基位置下标
            pos = random.randint(0, len(dna)-1)
            # 如果该位置已存在突变，重新随机选取位置直到不重复
            while pos in used_pos:
                pos = random.randint(0, len(dna)-1)
            # 将合法不重复突变位置加入集合记录
            used_pos.add(pos)
            # 获取该突变位置原始碱基
            old_base = dna[pos]
            # 调用工具函数生成不同的突变碱基
            new_base = _mutate_base(old_base)
            # 封装单条突变记录字典，加入突变总列表
            all_muts.append({
                "sequence_id": sid,
                "mutation_type": "SUBSTITUTION",
                "position": pos,
                "original_base": old_base,
                "new_base": new_base
            })
    # 传入输出路径时，将全部突变数据写入csv文件
    if output_file:
        _write_csv(output_file, all_muts, ["sequence_id", "mutation_type", "position", "original_base", "new_base"])
    # 返回全部突变记录列表供上层调用
    return all_muts


def generate_distances(sequences, output_file=None):
    # 集合推导式提取所有不重复物种名称，再转为列表存储
    species = list({s["species_name"] for s in sequences})
    # 空列表，存储所有物种/序列间的进化距离边数据
    dist_list = []
    # 1. 双重循环生成所有不同物种两两配对的距离关系
    for i in range(len(species)):
        # j从i+1开始，避免A-B和B-A重复生成相同物种对
        for j in range(i + 1, len(species)):
            # 取出当前配对的两个物种名称
            sp1, sp2 = species[i], species[j]
            # 判断是否属于近缘物种分组
            near_group = (i <= 1 and j <= 2) or (i >= len(species)-2 and j >= len(species)-1)
            # 判断是否属于远缘物种分组
            far_group = (i <= 1 and j >= len(species)-2) or (i >= len(species)-2 and j <= 1)
            # 近缘物种距离2~4
            if near_group:
                dist = random.randint(2, 4)
            # 远缘物种距离20~35
            elif far_group:
                dist = random.randint(20, 35)
            # 其余中等亲缘物种距离5~20
            else:
                dist = random.randint(5, 20)
            # 封装物种距离字典，存入距离总列表
            dist_list.append({"species_a": sp1, "species_b": sp2, "distance": dist})
    # 列表推导式提取全部序列ID，用于补充序列之间的距离边
    seq_ids = [s["sequence_id"] for s in sequences]
    # 循环补充序列间距离，保证总距离边数量不少于15条
    while len(dist_list) < 15:
        # 随机抽取两条不重复序列ID
        a, b = random.sample(seq_ids, 2)
        # 标记是否存在重复距离边
        duplicate = False
        # 遍历现有距离列表查重，正反配对都视为重复
        for d in dist_list:
            if (d["species_a"] == a and d["species_b"] == b) or (d["species_a"] == b and d["species_b"] == a):
                duplicate = True
                break
        # 存在重复边则跳过本次循环，重新生成配对
        if duplicate:
            continue
        # 生成0~1随机浮点数，划分距离区间概率
        r = random.random()
        # 30%概率生成近距离 1~4
        if r < 0.3:
            dist = random.randint(1, 4)
        # 30%概率生成远距离 21~40
        elif r > 0.7:
            dist = random.randint(21, 40)
        # 40%概率生成中等距离 5~20
        else:
            dist = random.randint(5, 20)
        # 封装序列间距离字典，添加进总距离列表
        dist_list.append({"species_a": a, "species_b": b, "distance": dist})
    # 传入输出路径时，将全部距离边写入csv文件
    if output_file:
        _write_csv(output_file, dist_list, ["species_a", "species_b", "distance"])
    # 返回完整距离边列表
    return dist_list


def generate_all_datasets(output_dir="datasets"):
    # 拼接序列数据集csv完整存储路径
    seq_path = os.path.join(output_dir, "sequences_dataset.csv")
    # 拼接突变数据集csv完整存储路径
    mut_path = os.path.join(output_dir, "mutations_dataset.csv")
    # 拼接进化距离数据集csv完整存储路径
    dist_path = os.path.join(output_dir, "evolutionary_distances_dataset.csv")
    # 调用序列生成函数，自动生成序列并写入对应csv文件
    seqs = generate_sequences(seq_path)
    # 传入序列数据，生成突变数据并写入突变csv
    muts = generate_mutations(seqs, mut_path)
    # 基于序列数据生成进化距离边，写入距离csv
    dists = generate_distances(seqs, dist_path)
    # 控制台打印生成序列总条数
    print(f"Generated {len(seqs)} sequences")
    # 控制台打印生成突变总条数
    print(f"Generated {len(muts)} mutations")
    # 控制台打印生成进化距离边总条数
    print(f"Generated {len(dists)} distance edges")
    # 控制台提示数据集保存文件夹路径
    print(f"Files saved to: {output_dir}/")
    # 一次性返回序列、突变、距离三组完整数据集，供外部加载函数使用
    return seqs, muts, dists