# 传承字形映射配置

提供一个 [《傳承字形標準化文件》](https://github.com/ichitenfont/inheritedglyphs) 中建议的字形映射配置文件。

## 能具体地说明解决了什么问题？

引用 [《傳承字形推薦形體表》](https://github.com/ichitenfont/inheritedglyphs/blob/master/table_of_recom_inherited_glyphs-1.04.pdf) 原文的表述：

> 我們強烈呼籲字型製作者以字理爲本，在製作傳承字形的字型時，不要盲從「原字集分離原則」這違反傳承字形原則的過時技術副產品。否則，若製作者只把「値」、「靑」、「爲」等傳承字形，放在 5024、9751、7232 這些正體（繁體）中文「事實標準」裏少用的碼位；至於正體（繁體）中文「事實標準」裏常用的碼位 503C、9752、70BA，卻放置着違反傳承字形規定的「值」、「青」、「為」等字形，只會令用戶容易踩中陷阱，誤用非傳承字形。這種做法顯然違反選擇傳承字形用戶之意願，絕不可取。

这个项目就是提供一个这样的配置文件，方便你使用一些工具和脚本快速处理上述问题。

## 配置文件的格式

配置文件在 [inherited-mapping.yaml](inherited-mapping.yaml)，是一个 [YAML](https://yaml.org/) 格式文件，结构示例如下：

```yaml
0x50DE:  # 僞
- 0x507D  # 偽
- 0x50DE  # 僞

0x514C:  # 兌
- 0x514C  # 兌
- 0x5151  # 兑
```

上面实际的含义为，将 0x507D、0x50DE 的字形映射到 0x50DE；将 0x514C、0x5151 的字形映射到 0x514C。

## 如何使用？

我们这里使用 `python` 来举例子。我们首先需要安装下面两个依赖：

- [FontTools](https://github.com/fonttools/fonttools)
- [PyYAML](https://github.com/yaml/pyyaml)

编写下面的代码：

```python
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
```
