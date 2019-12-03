from src.core import obfuscate, obfuscate_plus

if __name__ == '__main__':
    print(obfuscate('真0123456789好', '假6982075431的', 'test', False, 'test'))
    print(obfuscate_plus(
        '⓪⓵ⅱ③肆⓹㈥ⅦⅧ㊈谦锗孵塔瓤晰痔尖凯荤放国踌励拾卓侍猴补鹿德坪恶乙缺咯低谅骇绷曙赋睡矣凹陨详痪裹砍帜刀蟹泣搁诬拍宵茄氦汾确沈厢败匪零们摘漾掇叛概冕莫歌怀鸳喷顽碗脾冶家扒腕惋爹型谐男戈骂权疲洼不园崭烯',
        'test_plus', False, 'test'))
