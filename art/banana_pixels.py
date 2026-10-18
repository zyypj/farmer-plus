from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
TEXTURES = ROOT / 'common/src/main/resources/assets/farmerplus/textures'
PALETTE = {
    '.': '00000000', 'd': '294b28', 's': '386333', 'g': '467d39',
    'v': '599344', 'h': '73a854', 'r': '9ebd69', 'l': 'c4d58c',
    'a': '91a75b', 'b': 'b4bd73', 'c': 'dad6a0', 'e': 'f0e6bf',
    'o': '7b833f', 't': '80603d', 'k': '49352e', 'm': '654537',
    'w': '9e7947', 'p': 'c2a366', 'q': 'debe7c',
    'u': '3e1b31', 'n': '61243f', 'f': '84334f', 'j': 'a35269',
    'i': 'b97d8a', 'y': 'e4bd40', 'z': 'f4d868', 'x': 'b38d30',
    'A': '305731', 'B': '3b6b38', 'C': '477b3d', 'D': '538845',
    'E': '689950', 'F': '9bb973', 'G': '7ca357', 'H': 'c3d38f',
}
GRIDS = {
    'block/banana_stem': [
        'aaabbbbaaaaoaabb', 'aaabbbbaaaaoaabb', 'aaabbbbaamooaabb', 'aaabbbbaamkoaabb',
        'aaabbbbaamkoaabb', 'aaabbbbaaaaoaabb', 'maabbbbaaaaoaabb', 'kmabbbbaaaaoaabb',
        'kmaabbbamaaoaabb', 'mwaabbbmkmaoaabb', 'twaabbbmkmaoaabb', 'twaabbbammaoaabb',
        'twaabbbbaaaoaabb', 'twaabbbbaaaoaabb', 'twaabbbbaaaoaabb', 'twaabbbbaaaoaabb',
    ],
    'block/banana_stem_top': [
        'oooaaaaaaaaaaooo', 'ooaabbbbbbbbaaoo', 'oaabbccccccbbaao', 'aabbccbbbbccbbaa',
        'abbccbccccbccbba', 'abccbcceecbcccba', 'abcbccceecbcbbba', 'abcbceeeecbcbbba',
        'abcbceeeecbcbbba', 'abcbccceccbcbbba', 'abccbcccccbbccba', 'abbccbbbbbbccbba',
        'aabbccccccccbbaa', 'oaabbbbbbbbbbaao', 'ooaaaaaaaaaaaaoo', 'oooaaaaaaaaaaooo',
    ],
    'block/banana_leaf': [
        'BCCDEEEFHGDCCBBB', 'CDDDEEDFHGDCBBBA', '.BBCCDEFHGEDCCBB', '...CDEEFHGEDCB..',
        'BCCDEEEFHGDCBBBA', 'BCDDEEDFHGEDCCBB', 'CDDEEDDFHGDCC...', 'BCDDDEEFHGDCBBBA',
        'BBCCDEEFHGEDCCBB', '....DEEFHGDCBBBA', 'BCDDEEDFHGEDCCBB', 'CDDEEDDFHGDCCB..',
        '.BCDDEEFHGDCBBBA', 'BCCDEEEFHGEDCCBB', 'CDDDEEDFHGDCBBBA', 'BCCDEEEFHGDCCBBB',
    ],
    'block/banana_leaf_tip': [
        '.......FH.......', '......EFHG......', '.....DEFHGD.....', '....CDEFHGDC....',
        '...CDEEFHGEDC...', '..CDEEDFHGEDCB..', '.CDDEEDFHGEDCCB.', 'BCDDEEEFHGEDCCBB',
        'BCCDEEEFHGEDCCBB', '..DDEEDFHGDCBBBA', 'BCDDEEDFHGEDCCBB', 'CDDEEDDFHGDCCB..',
        'BBCCDEEFHGDCBBBA', 'BCDDEEEFHGEDCCBB', 'CDDDEEDFHGDCBBBA', 'BCCDEEEFHGDCCBBB',
    ],
    'block/banana_leaf_dry': [
        'wwppqqpqqpwwttmm', 'ppqqpppqqpwwttmm', '..ppwwwqqtww....', 'wwwwttwqqtmwtt..',
        '..wtttwqqtww....', '...wwppqqtwwt...', '....pppqqtmw....', '...ppwwqqtm.....',
        '....ttwqqtww....', '.....twqqtw.....', '......wqqtw.....', '.....pwqqt......',
        '......wqqt......', '.......qqt......', '.......qp.......', '.......q........',
    ],
    'block/banana_heart': [
        'fffjjjjjfffnnnuu', 'ffjiiiijjffnnuuu', 'ffjjjjjfffnnnuuu', 'nfffffffnnnnuuuu',
        'nnnffnnnnnuuuunn', 'ffnnnuuunnnfffjn', 'fjfffffffjjjffnn', 'fjjjjjjjjfffnnuu',
        'jjjfffffff nnnnuu'.replace(' ', ''), 'ffffnnnnnnnuuuuu', 'nnnnnuuuunnfffjn', 'fffjjjjjjjjffnnu',
        'ffjjjjjffffnnnuu', 'fffffff nnnnnuuuu'.replace(' ', ''), 'nnnffnnnnnuuuuuu', 'uunnnnnnuuuuuuuu',
    ],
    'block/banana_fingers_green': [
        'kkkkkkkkkkkkkkkk', 'sghvsghvsghvsghv', 'sghvsghvsghvsghv', 'sghvsghvsghvsghv',
        'sghvsghvsghvsghv', 'sghvsghvsghvsghv', 'sghvsghvsghvsghv', 'sggvsggvsggvsggv',
        'kkkkkkkkkkkkkkkk', 'sghvsghvsghvsghv', 'sghvsghvsghvsghv', 'sghvsghvsghvsghv',
        'sghvsghvsghvsghv', 'sghvsghvsghvsghv', 'sghvsghvsghvsghv', 'sggvsggvsggvsggv',
    ],
    'block/banana_fingers_ripe': [
        'kkkkkkkkkkkkkkkk', 'xyzyxyzyxyzyxyzy', 'xyzyxyzyxyzyxyzy', 'xyzyxyzyxyzyxyzy',
        'xyzyxykyxyzyxyzy', 'xyzyxyzyxyzyxyzy', 'xyzyxyzyxyzyxyzy', 'xyyyxyyyxyyyxyyy',
        'kkkkkkkkkkkkkkkk', 'xyzyxyzyxyzyxyzy', 'xyzyxyzyxyzyxyzy', 'xyzyxyzyxyzyxyzy',
        'xyzyxyzyxyzyxyky', 'xyzyxyzyxyzyxyzy', 'xyzyxyzyxyzyxyzy', 'xyyyxyyyxyyyxyyy',
    ],
    'block/banana_sapling': [
        '........r.......', '.......hl.......', '...r...hl.......', '...lh..rl...r...',
        '...lh..rl..rh...', '...vhg.rl..lh...', '....hgmrl..lh...', '....gvrlr.glg...',
        '.....vrlrvhv....', '.....gvrlrv.....', '......grlv......', '.......ba.......',
        '.......ba.......', '.......am.......', '......tba.......', '......taa.......',
    ],
    'item/banana': [
        '................', '............ot..', '...........aot..', '...........ayt..',
        '..........ozzt..', '..........ozzyt.', '.........ozzzyt.', '........ozzzyxt.',
        '......oozzzyyxt.', '....oozzzzyyxt..', '..ttozzzyyyxt...', '..txyyyyyyxt....',
        '...txxxxxtt.....', '.....tttt.......', '................', '................',
    ],
    'item/banana_leaf': [
        '................', '............r...', '..........vrl...', '........gvrlvg..',
        '......gvhrlvgg..', '.....gvhrlvggs..', '....gvhrlvggs...', '...gvhrlvgg.s...',
        '...vhrlvggss....', '..vhrlvggss.....', '..hrlvgg.s......', '..rlvgss........',
        '..lvgs..........', '.ar.............', '.a..............', '................',
    ],
}


def main():
    sheet = Image.new('RGBA', (660, 480), '#202c28')
    draw = ImageDraw.Draw(sheet)
    for index, (name, rows) in enumerate(GRIDS.items()):
        assert len(rows) == 16 and all(len(row) == 16 for row in rows), name
        image = Image.new('RGBA', (16, 16))
        for row, values in enumerate(rows):
            for column, token in enumerate(values):
                value = PALETTE[token]
                image.putpixel((column, row), tuple(bytes.fromhex(value)) if len(value) == 8 else tuple(bytes.fromhex(value)) + (255,))
        image.save(TEXTURES / (name + '.png'))
        left, top = 12 + index % 4 * 164, 12 + index // 4 * 156
        sheet.alpha_composite(image.resize((128, 128), Image.Resampling.NEAREST), (left, top))
        draw.text((left, top + 131), name.split('/')[-1].replace('banana_', ''), fill='#e5e9cd')
    destination = ROOT / 'docs/images/banana-textures.png'
    sheet.convert('RGB').save(destination)
    print(destination)


if __name__ == '__main__':
    main()
