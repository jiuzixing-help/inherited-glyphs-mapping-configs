import yaml
from fontTools.ttLib import TTFont


def main():
    # 加载配置
    with open('inherited-mapping.yaml', 'rb') as file:
        mapping: dict[int, list[int]] = yaml.safe_load(file)

    # 加载字体
    font = TTFont('ark-pixel-12px-proportional-zh_tr.otf')

    # 替换字体 cmap 映射
    cmap: dict[int, str] = font.getBestCmap()
    for target, code_points in mapping.items():
        if target not in cmap:
            continue
        glyph_name = cmap[target]
        for code_point in code_points:
            cmap[code_point] = glyph_name

    # 保存为新字体
    font.save('new-font.otf')


if __name__ == '__main__':
    main()
