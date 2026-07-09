# src/visualisation/html_visualizer.py
"""
Part 2 Task 5: HTML Visualization
生成包含序列查看器、突变历史、系统发育图(MST)、序列比对、热点检测的交互式HTML页面
"""

import json
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
_root = Path(__file__).parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from src.data.dataset_generator import generate_all_datasets
from src.data.data_loader import load_all_datasets
from src.visualisation.MST_graph import PhylogeneticGraph as MSTPhyloGraph
from src.analysis.edit_distance import compute_edit_distance, traceback, get_alignment_from_stack
from src.analysis.hotspot_detection import detect_hotspots, detect_hotspots_from_multiple_alignments


def generate_html(output_file="visualization.html", data_dir="datasets"):
    """
    生成完整的HTML可视化页面
    
    Args:
        output_file: 输出HTML文件名
        data_dir: 数据集目录
    
    Returns:
        str: 生成的HTML文件路径
    """
    
    # ============================================================
    # 1. 生成并加载数据
    # ============================================================
    print("Generating dataset...")
    generate_all_datasets(data_dir)
    
    print("Loading dataset...")
    sequences_dict, mutations_list, graph = load_all_datasets(data_dir)
    
    sequences = list(sequences_dict.values())
    
    # ============================================================
    # 2. 计算 MST
    # ============================================================
    print("Computing MST...")
    mst_graph = MSTPhyloGraph()
    
    # 从 graph 复制边到 mst_graph
    for edge in graph.edges:
        mst_graph.add_relationship(edge[0], edge[1], edge[2])
    
    mst = mst_graph.compute_mst()
    
    # ============================================================
    # 3. 准备序列数据（用于序列查看器）
    # ============================================================
    seq_data = []
    for seq in sequences:
        seq_data.append({
            'id': seq.sequence_id,
            'species': seq.species_name,
            'sequence': seq.get_sequence_string(),
            'length': seq.length(),
            'mutations': [
                {
                    'type': m.mutation_type.value,
                    'position': m.position,
                    'original': m.original_base.value if m.original_base else '-',
                    'new': m.new_base.value if m.new_base else '-'
                }
                for m in seq.mutation_history()
            ]
        })
    
    # ============================================================
    # 4. 准备图数据（用于系统发育图）
    # ============================================================
    species_list = graph.species
    edges_list = graph.edges
    mst_edges_list = mst.edges
    
    # 标记哪些边属于MST
    mst_edge_set = set()
    for u, v, _ in mst_edges_list:
        mst_edge_set.add((u, v))
        mst_edge_set.add((v, u))
    
    graph_data = {
        'species': species_list,
        'edges': edges_list,
        'mst_edges': mst_edges_list,
        'mst_edge_set': list(mst_edge_set)
    }
    
    # ============================================================
    # 5. 准备编辑距离数据
    # ============================================================
    edit_distance_data = {}
    for i, s1 in enumerate(sequences):
        for j, s2 in enumerate(sequences):
            if i < j:
                key = f"{s1.sequence_id}--{s2.sequence_id}"
                dp = compute_edit_distance(s1, s2)
                dist, stack = traceback(s1, s2, dp)
                aligned_a, aligned_b, ops = get_alignment_from_stack(stack)
                edit_distance_data[key] = {
                    'seq1_id': s1.sequence_id,
                    'seq2_id': s2.sequence_id,
                    'distance': dist,
                    'aligned_a': aligned_a,
                    'aligned_b': aligned_b,
                    'operations': ops
                }
    
    # ============================================================
    # 6. 准备热点检测数据
    # ============================================================
    hotspot_data = {}
    species_set = set(seq.species_name for seq in sequences)
    for species in species_set:
        species_seqs = [s for s in sequences if s.species_name == species]
        if len(species_seqs) > 1:
            hotspots = detect_hotspots_from_multiple_alignments(species_seqs, threshold=0.3)
            hotspot_data[species] = hotspots
    
    # ============================================================
    # 7. 生成 HTML
    # ============================================================
    seq_ids = [s['id'] for s in seq_data]
    seq_options = '\n'.join(f'<option value="{s}">{s}</option>' for s in seq_ids)
    seq_json = json.dumps(seq_data)
    graph_json = json.dumps(graph_data)
    edit_json = json.dumps(edit_distance_data)
    hotspot_json = json.dumps(hotspot_data)
    
    html_content = _generate_html_template()
    
    # 替换所有占位符
    html_content = html_content.replace('{{seq_options}}', seq_options)
    html_content = html_content.replace('{{seq_json}}', seq_json)
    html_content = html_content.replace('{{graph_json}}', graph_json)
    html_content = html_content.replace('{{edit_json}}', edit_json)
    html_content = html_content.replace('{{hotspot_json}}', hotspot_json)
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML visualization saved to: {output_file}")
    return output_file


def _generate_html_template():
    """生成HTML模板（纯字符串，所有占位符用双花括号）"""
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>生物信息学分析工具 - 可视化界面</title>
    <style>
        /* ===== 全局样式 ===== */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f4f8;
            padding: 20px;
            color: #2d3748;
        }}
        
        h1 {{
            text-align: center;
            color: #2b6cb0;
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            text-align: center;
            color: #718096;
            font-size: 14px;
            margin-bottom: 30px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        /* ===== 面板样式 ===== */
        .panel {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            padding: 20px;
            margin-bottom: 25px;
        }}
        
        .panel h2 {{
            color: #2b6cb0;
            font-size: 18px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        
        .panel h2 .badge {{
            font-size: 12px;
            background: #2b6cb0;
            color: white;
            padding: 2px 10px;
            border-radius: 12px;
            margin-left: 8px;
        }}
        
        .row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        @media (max-width: 900px) {{
            .row {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* ===== 序列查看器 ===== */
        .nucleotide-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            padding: 10px;
            background: #f7fafc;
            border-radius: 8px;
            min-height: 50px;
            margin-top: 10px;
        }}
        
        .nucleotide {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 13px;
            color: white;
            transition: transform 0.2s;
            cursor: default;
        }}
        
        .nucleotide:hover {{
            transform: scale(1.15);
        }}
        
        .nucleotide.A {{ background: #e53e3e; }}
        .nucleotide.T {{ background: #38a169; }}
        .nucleotide.G {{ background: #2b6cb0; }}
        .nucleotide.C {{ background: #d69e2e; }}
        
        /* ===== 下拉框和按钮 ===== */
        select, button {{
            padding: 8px 16px;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            font-size: 14px;
            background: white;
            outline: none;
            cursor: pointer;
        }}
        
        select:focus, button:focus {{
            border-color: #2b6cb0;
            box-shadow: 0 0 0 3px rgba(43,108,176,0.2);
        }}
        
        button {{
            background: #2b6cb0;
            color: white;
            border: none;
            transition: background 0.2s;
        }}
        
        button:hover {{
            background: #1a4f8b;
        }}
        
        .select-group {{
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }}
        
        /* ===== 突变历史 ===== */
        .mutation-list {{
            max-height: 150px;
            overflow-y: auto;
            font-size: 13px;
            background: #f7fafc;
            padding: 10px;
            border-radius: 8px;
        }}
        
        .mutation-item {{
            padding: 3px 0;
            border-bottom: 1px solid #edf2f7;
            font-family: monospace;
        }}
        
        .mutation-item:last-child {{
            border-bottom: none;
        }}
        
        /* ===== 图 ===== */
        .graph-container {{
            position: relative;
            width: 100%;
            height: 420px;
            background: #f7fafc;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            overflow: hidden;
        }}
        
        .node {{
            position: absolute;
            padding: 6px 14px;
            background: #2b6cb0;
            color: white;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-align: center;
            transform: translate(-50%, -50%);
            cursor: default;
            z-index: 10;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }}
        
        .edge {{
            position: absolute;
            height: 2px;
            background: #a0aec0;
            transform-origin: left center;
            z-index: 1;
        }}
        
        .edge.mst {{
            background: #e53e3e;
            height: 3px;
            z-index: 2;
        }}
        
        .edge-label {{
            position: absolute;
            background: white;
            padding: 1px 8px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: bold;
            color: #4a5568;
            border: 1px solid #e2e8f0;
            transform: translate(-50%, -50%);
            z-index: 5;
        }}
        
        .graph-controls {{
            margin-bottom: 10px;
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        /* ===== 比对结果 ===== */
        .alignment-box {{
            background: #1a202c;
            color: #e2e8f0;
            padding: 12px 16px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            overflow-x: auto;
            white-space: pre;
            line-height: 1.6;
            margin-top: 8px;
        }}
        
        .distance-result {{
            font-size: 20px;
            font-weight: bold;
            color: #e53e3e;
            margin: 8px 0;
        }}
        
        /* ===== 热点检测 ===== */
        .hotspot-item {{
            padding: 8px 12px;
            background: #f7fafc;
            border-radius: 6px;
            margin-bottom: 6px;
            border-left: 4px solid #e53e3e;
        }}
        
        .hotspot-item strong {{
            color: #2b6cb0;
        }}
        
        /* ===== 统计数据 ===== */
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 12px;
            margin-bottom: 15px;
        }}
        
        .stat-card {{
            background: #f7fafc;
            padding: 12px 16px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-card .num {{
            font-size: 24px;
            font-weight: bold;
            color: #2b6cb0;
        }}
        
        .stat-card .label {{
            font-size: 12px;
            color: #718096;
        }}
        
        /* ===== 空状态 ===== */
        .empty-state {{
            color: #a0aec0;
            text-align: center;
            padding: 20px;
            font-style: italic;
        }}
        
        /* ===== 加载提示 ===== */
        .loading {{
            text-align: center;
            padding: 30px;
            color: #718096;
        }}
    </style>
</head>
<body>

<div class="container">
    <h1>🧬 生物信息学分析工具</h1>
    <p class="subtitle">Interactive Bioinformatics Analysis Tool — Part 2 Task 5</p>
    
    <!-- ============================================================ -->
    <!-- 统计信息 -->
    <!-- ============================================================ -->
    <div class="panel">
        <h2>📊 数据集概览</h2>
        <div class="stats" id="stats-container">
            <div class="stat-card"><div class="num" id="stat-seqs">0</div><div class="label">序列数</div></div>
            <div class="stat-card"><div class="num" id="stat-species">0</div><div class="label">物种数</div></div>
            <div class="stat-card"><div class="num" id="stat-edges">0</div><div class="label">进化关系</div></div>
            <div class="stat-card"><div class="num" id="stat-mst">0</div><div class="label">MST 边数</div></div>
        </div>
    </div>
    
    <!-- ============================================================ -->
    <!-- 序列查看器 + 突变历史 -->
    <!-- ============================================================ -->
    <div class="row">
        <div class="panel">
            <h2>🔬 序列查看器</h2>
            <div class="select-group">
                <label>选择序列：</label>
                <select id="seq-select" onchange="updateViewer()">
                    {{seq_options}}
                </select>
                <span style="font-size:13px;color:#718096;" id="seq-info"></span>
            </div>
            <div class="nucleotide-container" id="seq-display">
                <div class="empty-state">请选择序列</div>
            </div>
        </div>
        
        <div class="panel">
            <h2>📜 突变历史</h2>
            <div id="mutation-history" class="mutation-list">
                <div class="empty-state">请选择序列查看突变</div>
            </div>
        </div>
    </div>
    
    <!-- ============================================================ -->
    <!-- 系统发育图 + MST -->
    <!-- ============================================================ -->
    <div class="panel">
        <h2>🌳 系统发育图 <span class="badge">MST 红色高亮</span></h2>
        <div class="graph-controls">
            <button id="btn-toggle-mst" onclick="toggleMST()">🔴 仅显示 MST</button>
            <span style="font-size:13px;color:#718096;" id="mst-info"></span>
        </div>
        <div class="graph-container" id="graph-container"></div>
    </div>
    
    <!-- ============================================================ -->
    <!-- 序列比对 -->
    <!-- ============================================================ -->
    <div class="panel">
        <h2>📋 序列比对 <span class="badge">编辑距离</span></h2>
        <div class="select-group" style="margin-bottom:12px;">
            <label>序列 A：</label>
            <select id="align-seq1">{{seq_options}}</select>
            <label>序列 B：</label>
            <select id="align-seq2">{{seq_options}}</select>
            <button onclick="compareSequences()">🔍 比对</button>
        </div>
        <div id="align-result">
            <div class="empty-state">选择两条序列后点击"比对"</div>
        </div>
    </div>
    
    <!-- ============================================================ -->
    <!-- 热点检测 -->
    <!-- ============================================================ -->
    <div class="panel">
        <h2>🔥 突变热点检测 <span class="badge">阈值 30%</span></h2>
        <div id="hotspot-container">
            <div class="loading">加载热点数据...</div>
        </div>
    </div>
</div>

<script>
    // ============================================================
    // 数据（由 Python 注入）
    // ============================================================
    const sequences = {{seq_json}};
    const graphData = {{graph_json}};
    const editData = {{edit_json}};
    const hotspotData = {{hotspot_json}};
    
    let showMSTOnly = false;
    let mstEdges = new Set();
    if (graphData.mst_edge_set) {{
        graphData.mst_edge_set.forEach(pair => {{
            mstEdges.add(pair.join('--'));
        }});
    }}
    
    // ============================================================
    // 初始化
    // ============================================================
    document.addEventListener('DOMContentLoaded', function() {{
        updateStats();
        updateViewer();
        drawGraph();
        renderHotspots();
    }});
    
    // ============================================================
    // 更新统计信息
    // ============================================================
    function updateStats() {{
        document.getElementById('stat-seqs').textContent = sequences.length;
        const species = new Set(sequences.map(s => s.species));
        document.getElementById('stat-species').textContent = species.size;
        document.getElementById('stat-edges').textContent = graphData.edges ? graphData.edges.length : 0;
        document.getElementById('stat-mst').textContent = graphData.mst_edges ? graphData.mst_edges.length : 0;
    }}
    
    // ============================================================
    // 序列查看器
    // ============================================================
    function updateViewer() {{
        const select = document.getElementById('seq-select');
        const id = select.value;
        const seq = sequences.find(s => s.id === id);
        if (!seq) return;
        
        document.getElementById('seq-info').textContent = 
            '物种: ' + seq.species + ' | 长度: ' + seq.length;
        
        const container = document.getElementById('seq-display');
        container.innerHTML = '';
        for (let i = 0; i < seq.sequence.length; i++) {{
            const base = seq.sequence[i];
            const div = document.createElement('div');
            div.className = 'nucleotide ' + base;
            div.textContent = base;
            div.title = '位置 ' + i;
            container.appendChild(div);
        }}
        
        renderMutations(seq);
    }}
    
    // ============================================================
    // 突变历史
    // ============================================================
    function renderMutations(seq) {{
        const container = document.getElementById('mutation-history');
        if (!seq.mutations || seq.mutations.length === 0) {{
            container.innerHTML = '<div class="empty-state">无突变记录</div>';
            return;
        }}
        let html = '';
        const sorted = [...seq.mutations].reverse();
        for (const m of sorted) {{
            const icon = m.type === 'INSERTION' ? '➕' : m.type === 'DELETION' ? '➖' : '🔄';
            html += '<div class="mutation-item">' + icon + ' [' + m.type + '] 位置 ' + m.position + ' : ' + m.original + ' → ' + m.new + '</div>';
        }}
        container.innerHTML = html;
    }}
    
    // ============================================================
    // 系统发育图
    // ============================================================
    function drawGraph() {{
        const container = document.getElementById('graph-container');
        const width = container.offsetWidth || 800;
        const height = container.offsetHeight || 400;
        container.innerHTML = '';
        
        const species = graphData.species;
        if (!species || species.length === 0) {{
            container.innerHTML = '<div class="empty-state" style="line-height:400px;">无物种数据</div>';
            return;
        }}
        
        const cx = width / 2;
        const cy = height / 2;
        const radius = Math.min(width, height) / 2.8;
        const positions = {{}};
        for (let i = 0; i < species.length; i++) {{
            const angle = (i / species.length) * 2 * Math.PI - Math.PI / 2;
            positions[species[i]] = {{
                x: cx + radius * Math.cos(angle),
                y: cy + radius * Math.sin(angle)
            }};
        }}
        
        const edges = showMSTOnly ? graphData.mst_edges : graphData.edges;
        if (edges) {{
            for (const edge of edges) {{
                const u = edge[0], v = edge[1], w = edge[2];
                if (!positions[u] || !positions[v]) continue;
                const isMST = mstEdges.has(u + '--' + v) || mstEdges.has(v + '--' + u);
                if (showMSTOnly && !isMST) continue;
                
                const x1 = positions[u].x, y1 = positions[u].y;
                const x2 = positions[v].x, y2 = positions[v].y;
                const len = Math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1));
                const angleDeg = Math.atan2(y2-y1, x2-x1) * 180 / Math.PI;
                
                const line = document.createElement('div');
                line.className = 'edge' + (isMST ? ' mst' : '');
                line.style.left = x1 + 'px';
                line.style.top = y1 + 'px';
                line.style.width = len + 'px';
                line.style.transform = 'rotate(' + angleDeg + 'deg)';
                container.appendChild(line);
                
                const label = document.createElement('div');
                label.className = 'edge-label';
                label.textContent = w;
                label.style.left = ((x1+x2)/2) + 'px';
                label.style.top = ((y1+y2)/2 - 12) + 'px';
                container.appendChild(label);
            }}
        }}
        
        for (const sp of species) {{
            const pos = positions[sp];
            const node = document.createElement('div');
            node.className = 'node';
            node.textContent = sp;
            node.style.left = pos.x + 'px';
            node.style.top = pos.y + 'px';
            container.appendChild(node);
        }}
        
        let totalWeight = 0;
        if (graphData.mst_edges) {{
            for (const e of graphData.mst_edges) totalWeight += e[2];
        }}
        document.getElementById('mst-info').textContent = 
            'MST: ' + (graphData.mst_edges ? graphData.mst_edges.length : 0) + ' 条边, 总权重 ' + totalWeight;
    }}
    
    function toggleMST() {{
        showMSTOnly = !showMSTOnly;
        document.getElementById('btn-toggle-mst').textContent = 
            showMSTOnly ? '🔵 显示全部' : '🔴 仅显示 MST';
        drawGraph();
    }}
    
    // ============================================================
    // 序列比对
    // ============================================================
    function compareSequences() {{
        const id1 = document.getElementById('align-seq1').value;
        const id2 = document.getElementById('align-seq2').value;
        const container = document.getElementById('align-result');
        
        if (id1 === id2) {{
            container.innerHTML = '<div class="empty-state">请选择两条不同的序列</div>';
            return;
        }}
        
        const key1 = id1 + '--' + id2;
        const key2 = id2 + '--' + id1;
        let data = editData[key1] || editData[key2];
        
        if (!data) {{
            container.innerHTML = '<div class="empty-state">未找到比对数据</div>';
            return;
        }}
        
        let marks = '';
        for (let i = 0; i < data.aligned_a.length; i++) {{
            if (data.aligned_a[i] === data.aligned_b[i]) {{
                marks += '|';
            }} else if (data.aligned_a[i] === '-' || data.aligned_b[i] === '-') {{
                marks += ' ';
            }} else {{
                marks += '*';
            }}
        }}
        
        let html = '<div class="distance-result">📏 编辑距离: ' + data.distance + '</div>';
        html += '<div class="alignment-box">' + data.aligned_a + '</div>';
        html += '<div class="alignment-box" style="color:#a0aec0;">' + marks + '</div>';
        html += '<div class="alignment-box">' + data.aligned_b + '</div>';
        html += '<div style="margin-top:8px;font-size:12px;color:#718096;">操作: ' + data.operations.join(' → ') + '</div>';
        container.innerHTML = html;
    }}
    
    // ============================================================
    // 热点检测
    // ============================================================
    function renderHotspots() {{
        const container = document.getElementById('hotspot-container');
        const species = Object.keys(hotspotData);
        
        if (species.length === 0) {{
            container.innerHTML = '<div class="empty-state">无热点数据（需要同一物种多条序列）</div>';
            return;
        }}
        
        let html = '';
        for (const sp of species) {{
            const hotspots = hotspotData[sp];
            html += '<h3 style="margin:12px 0 8px;color:#2d3748;">🧬 ' + sp + '</h3>';
            if (hotspots.length === 0) {{
                html += '<div class="empty-state" style="padding:8px;">无热点 (阈值30%)</div>';
                continue;
            }}
            for (const h of hotspots) {{
                const div = (h.diversity * 100).toFixed(1);
                html += '<div class="hotspot-item">';
                html += '<strong>位置 ' + h.position + '</strong> — ';
                html += '多样性 ' + div + '% | ';
                html += '主要碱基: ' + h.majority_base + ' | ';
                html += '次要碱基: ' + h.minority_base;
                html += '<span style="color:#718096;font-size:12px;margin-left:10px;">';
                html += 'A:' + h.base_counts.A + ' T:' + h.base_counts.T + ' G:' + h.base_counts.G + ' C:' + h.base_counts.C;
                html += '</span></div>';
            }}
        }}
        container.innerHTML = html;
    }}
    
    window.addEventListener('resize', drawGraph);
</script>

</body>
</html>
'''


def generate_html_with_existing_data(sequences, graph, sequence_library, output_file="visualization.html"):
    """
    使用已有数据生成HTML（用于从main.py调用）
    
    Args:
        sequences: Sequence对象列表
        graph: PhylogeneticGraph对象
        sequence_library: SequenceLibrary对象
        output_file: 输出文件名
    """
    # 重新打包数据
    seq_data = []
    for seq in sequences:
        seq_data.append({
            'id': seq.sequence_id,
            'species': seq.species_name,
            'sequence': seq.get_sequence_string(),
            'length': seq.length(),
            'mutations': [
                {
                    'type': m.mutation_type.value,
                    'position': m.position,
                    'original': m.original_base.value if m.original_base else '-',
                    'new': m.new_base.value if m.new_base else '-'
                }
                for m in seq.mutation_history()
            ]
        })
    
    # 计算MST
    mst_graph = MSTPhyloGraph()
    for edge in graph.edges:
        mst_graph.add_relationship(edge[0], edge[1], edge[2])
    mst = mst_graph.compute_mst()
    
    mst_edge_set = set()
    for u, v, _ in mst.edges:
        mst_edge_set.add((u, v))
        mst_edge_set.add((v, u))
    
    graph_data = {
        'species': graph.species,
        'edges': graph.edges,
        'mst_edges': mst.edges,
        'mst_edge_set': list(mst_edge_set)
    }
    
    # 编辑距离
    edit_data = {}
    for i, s1 in enumerate(sequences):
        for j, s2 in enumerate(sequences):
            if i < j:
                key = f"{s1.sequence_id}--{s2.sequence_id}"
                dp = compute_edit_distance(s1, s2)
                dist, stack = traceback(s1, s2, dp)
                aligned_a, aligned_b, ops = get_alignment_from_stack(stack)
                edit_data[key] = {
                    'seq1_id': s1.sequence_id,
                    'seq2_id': s2.sequence_id,
                    'distance': dist,
                    'aligned_a': aligned_a,
                    'aligned_b': aligned_b,
                    'operations': ops
                }
    
    # 热点检测
    hotspot_data = {}
    species_set = set(seq.species_name for seq in sequences)
    for species in species_set:
        species_seqs = [s for s in sequences if s.species_name == species]
        if len(species_seqs) > 1:
            hotspots = detect_hotspots_from_multiple_alignments(species_seqs, threshold=0.3)
            hotspot_data[species] = hotspots
    
    # 生成HTML
    seq_ids = [s['id'] for s in seq_data]
    seq_options = '\n'.join(f'<option value="{s}">{s}</option>' for s in seq_ids)
    seq_json = json.dumps(seq_data)
    graph_json = json.dumps(graph_data)
    edit_json = json.dumps(edit_data)
    hotspot_json = json.dumps(hotspot_data)
    
    html_content = _generate_html_template()
    html_content = html_content.replace('{{seq_options}}', seq_options)
    html_content = html_content.replace('{{seq_json}}', seq_json)
    html_content = html_content.replace('{{graph_json}}', graph_json)
    html_content = html_content.replace('{{edit_json}}', edit_json)
    html_content = html_content.replace('{{hotspot_json}}', hotspot_json)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML visualization saved to: {output_file}")
    return output_file


if __name__ == "__main__":
    generate_html()