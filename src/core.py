import random
import traceback

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

from config import NAME_STRING, BASE_FONT_FILE
from src.utils import str_has_whitespace, str_has_emoji, deduplicate_str, ensure_cmap_has_all_text, subset_ttf_font, \
    get_project_root

root = get_project_root()


def obfuscate(plain_text, shadow_text, filename: str, only_ttf: bool, target_path: str = 'output') -> dict:
    """
    :param plain_text: 用户看到的内容
    :param shadow_text: 爬虫看到的内容
    :param filename: 不含格式后缀的文件名
    :param only_ttf: 是否需要woff、woff2格式
    :param target_path: 生成的目标目录
    """

    if str_has_whitespace(plain_text) | str_has_whitespace(shadow_text):
        raise Exception('明文或阴书不允许含有空格')

    if str_has_emoji(plain_text) | str_has_emoji(shadow_text):
        raise Exception('明文或阴书不允许含有emoji')

    plain_text = deduplicate_str(plain_text)
    shadow_text = deduplicate_str(shadow_text)

    if plain_text == shadow_text:
        raise Exception('没有意义的混淆')

    if len(plain_text) != len(shadow_text):
        raise Exception('阴书的有效长度需与明文一致')

    original_font = TTFont(root / BASE_FONT_FILE)
    # https://github.com/fonttools/fonttools/blob/4.0.1/Lib/fontTools/fontBuilder.py#L28

    # <class 'dict'>: {32: 'cid00001', 33: 'cid00002', 34: 'cid00003'...}
    # key 为 ord(字符串)
    original_cmap: dict = original_font.getBestCmap()

    try:
        ensure_cmap_has_all_text(original_cmap, plain_text)
    except Exception as e:
        raise e

    # print('plain_text', plain_text)
    # print('shadow_text', shadow_text)

    glyphs, metrics, cmap = {}, {}, {}

    # https://github.com/fonttools/fonttools/blob/4.0.1/Tests/pens/ttGlyphPen_test.py#L21
    glyph_set = original_font.getGlyphSet()

    pen = TTGlyphPen(glyph_set)

    glyph_order = original_font.getGlyphOrder()

    # print('glyph_order', glyph_order)

    final_shadow_text: list = []

    if 'null' in glyph_order:
        # print('基础字体含有 null')
        glyph_set['null'].draw(pen)
        glyphs['null'] = pen.glyph()
        metrics['null'] = original_font['hmtx']['null']

        final_shadow_text += ['null']

    if '.notdef' in glyph_order:
        # print('基础字体含有 .notdef')
        glyph_set['.notdef'].draw(pen)
        glyphs['.notdef'] = pen.glyph()
        metrics['.notdef'] = original_font['hmtx']['.notdef']

        final_shadow_text += ['.notdef']

    for index, (plain, shadow) in enumerate(zip(plain_text, shadow_text)):
        # print('index', index, 'plain', plain, 'shadow', shadow)

        shadow_cmap_name = original_cmap[ord(shadow)]
        # print('shadow_cmap_name', shadow_cmap_name)

        final_shadow_text += [shadow_cmap_name]

        glyph_set[original_cmap[ord(plain)]].draw(pen)
        glyphs[shadow_cmap_name] = pen.glyph()

        metrics[shadow_cmap_name] = original_font['hmtx'][original_cmap[ord(plain)]]

        cmap[ord(shadow)] = shadow_cmap_name

    # print('cmap', cmap)
    # print('metrics', metrics)
    # print('final_shadow_text', final_shadow_text)

    horizontal_header = {
        'ascent': original_font['hhea'].ascent,
        'descent': original_font['hhea'].descent,
    }

    fb = FontBuilder(original_font['head'].unitsPerEm, isTTF=True)
    fb.setupGlyphOrder(final_shadow_text)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(**horizontal_header)
    fb.setupNameTable(NAME_STRING)
    fb.setupOS2()
    fb.setupPost()
    # print('创建了新字体文件', f'{target_path}/{filename}.ttf')
    fb.save(f'{root}/{target_path}/{filename}.ttf')
    # print('创建了新字体文件', f'{target_path}/{filename}.ttf')

    result = dict()
    result['ttf'] = f'{root}/{target_path}/{filename}.ttf'

    if not only_ttf:
        woff_and_woff2 = subset_ttf_font(f'{root}/{target_path}/{filename}')
        result = {**result, **woff_and_woff2}

    return result


# name混淆加强版
def obfuscate_plus(plain_text, filename: str, only_ttf: bool, target_path: str = 'output'):
    """
    :param plain_text: 用户看到的内容
    :param filename: 不含格式后缀的文件名
    :param only_ttf: 是否需要woff、woff2格式
    :param target_path: 生成的目标目录
    """

    if str_has_whitespace(plain_text):
        raise Exception('明文不允许含有空格')

    if str_has_emoji(plain_text):
        raise Exception('明文不允许含有emoji')

    plain_text = deduplicate_str(plain_text)

    original_font = TTFont(root / BASE_FONT_FILE)
    # https://github.com/fonttools/fonttools/blob/4.0.1/Lib/fontTools/fontBuilder.py#L28

    # <class 'dict'>: {32: 'cid00001', 33: 'cid00002', 34: 'cid00003'...}
    # key 为 ord(字符串)
    original_cmap: dict = original_font.getBestCmap()

    try:
        ensure_cmap_has_all_text(original_cmap, plain_text)
    except Exception as e:
        raise e

    # print('plain_text', plain_text)

    glyphs, metrics, cmap = {}, {}, {}

    # Unicode字符平面映射
    # https://zh.wikipedia.org/wiki/Unicode%E5%AD%97%E7%AC%A6%E5%B9%B3%E9%9D%A2%E6%98%A0%E5%B0%84
    private_codes = random.sample(range(0xE000, 0xF8FF), len(plain_text))

    # 中文汉字和常见英文数字等的unicode编码范围实例页面
    # https://www.zhangxinxu.com/study/201611/chinese-language-unicode-range.html
    cjk_codes = random.sample(range(0x4E00, 0x9FA5), len(plain_text))

    # print('private_codes', private_codes)
    # print('cjk_codes', cjk_codes)

    # https://github.com/fonttools/fonttools/blob/4.0.1/Tests/pens/ttGlyphPen_test.py#L21
    glyph_set = original_font.getGlyphSet()

    pen = TTGlyphPen(glyph_set)

    glyph_order = original_font.getGlyphOrder()

    # print('glyph_order', glyph_order)

    final_shadow_text: list = []

    if 'null' in glyph_order:
        # print('基础字体含有 null')
        glyph_set['null'].draw(pen)
        glyphs['null'] = pen.glyph()
        metrics['null'] = original_font['hmtx']['null']

        final_shadow_text += ['null']

    if '.notdef' in glyph_order:
        # print('基础字体含有 .notdef')
        glyph_set['.notdef'].draw(pen)
        glyphs['.notdef'] = pen.glyph()
        metrics['.notdef'] = original_font['hmtx']['.notdef']

        final_shadow_text += ['.notdef']

    html_entities = []

    # 理论上这里还可以再打散一次顺序
    for index, plain in enumerate(plain_text):
        # print('index', index, 'plain', plain)

        try:
            shadow_cmap_name = original_cmap[cjk_codes[index]]
            # print('shadow_cmap_name', shadow_cmap_name)
        except KeyError:
            # 遇到基础字库不存在的字会出现这种错误
            traceback.print_exc()
            return obfuscate_plus(filename, plain_text, only_ttf, target_path)

        final_shadow_text += [shadow_cmap_name]

        glyph_set[original_cmap[ord(plain)]].draw(pen)
        glyphs[shadow_cmap_name] = pen.glyph()

        metrics[shadow_cmap_name] = original_font['hmtx'][original_cmap[ord(plain)]]

        cmap[private_codes[index]] = shadow_cmap_name
        html_entities += [hex(private_codes[index]).replace('0x', '&#x')]

    # print('cmap', cmap)
    # print('metrics', metrics)
    # print('final_shadow_text', final_shadow_text)
    # print('html_entities', html_entities)

    horizontal_header = {
        'ascent': original_font['hhea'].ascent,
        'descent': original_font['hhea'].descent,
    }

    fb = FontBuilder(original_font['head'].unitsPerEm, isTTF=True)
    fb.setupGlyphOrder(final_shadow_text)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(**horizontal_header)
    fb.setupNameTable(NAME_STRING)
    fb.setupOS2()
    fb.setupPost()
    fb.save(f'{root}/{target_path}/{filename}.ttf')
    # print('创建了新字体文件', f'{root}/{target_path}/{filename}.ttf')

    result = dict()
    result['ttf'] = f'{root}/{target_path}/{filename}.ttf'

    if only_ttf:
        return result
    else:
        woff_and_woff2 = subset_ttf_font(f'{root}/{target_path}/{filename}')
        return {**result, **woff_and_woff2}, dict(zip(plain_text, html_entities))
