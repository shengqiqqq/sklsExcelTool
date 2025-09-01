class ExcelColumn:
    """
    模拟Excel列名的26进制对象类

    Excel列名采用特殊的26进制表示法：
    - A-Z 分别表示 1-26
    - AA表示27，AB表示28，依此类推
    """

    def __init__(self, value):
        """
        初始化Excel列对象

        参数:
            value: 可以是列名(如"A", "B", "AA")或数字(如1, 2, 27)
            兼容小写了
        """
        if isinstance(value, str):
            # 确保输入是有效的列名

            if not value.isalpha():
                raise ValueError(f"无效的Excel列名:{value}")
            self.name = value.upper()
            self.number = self._name_to_number(value)
        elif isinstance(value, int):
            if value <= 0:
                raise ValueError(f"错误的数字:{value}。Excel列号必须是正数")
            self.number = value
            self.name = self._number_to_name(value)
        else:
            raise TypeError(f"无效的值类型:{type(value)}。值必须是字符串或整数")

    def _name_to_number(self, name):
        """将列名转换为对应的数字"""
        number = 0
        name = name.upper()
        for char in name:
            number = number * 26 + (ord(char) - ord('A') + 1)
        return number

    def _number_to_name(self, number):
        """将数字转换为对应的列名"""
        name = ""
        while number > 0:
            # 调整为0-25的范围(因为Excel列没有0)
            number -= 1
            # 取余得到当前位
            remainder = number % 26
            # 转换为字符
            name = chr(ord('A') + remainder) + name
            # 整除26
            number = number // 26
        return name

    def __add__(self, other):
        """加法运算"""
        if isinstance(other, ExcelColumn):
            return ExcelColumn(self.number + other.number)
        elif isinstance(other, int):
            return ExcelColumn(self.number + other)
        else:
            raise TypeError(f"不支持的加法操作数类型: {type(other)}")

    def __sub__(self, other):
        """减法运算"""
        if isinstance(other, ExcelColumn):
            result = self.number - other.number
        elif isinstance(other, int):
            result = self.number - other
        else:
            raise TypeError(f"不支持的减法操作数类型: {type(other)}")

        if result <= 0:
            raise ValueError(f"不支持的算数结果:{result}。减法结果必须是正数")
        return ExcelColumn(result)

    def __lt__(self, other):
        """小于比较"""
        if isinstance(other, ExcelColumn):
            return self.number < other.number
        elif isinstance(other, int):
            return self.number < other
        else:
            return NotImplemented

    def __le__(self, other):
        """小于等于比较"""
        if isinstance(other, ExcelColumn):
            return self.number <= other.number
        elif isinstance(other, int):
            return self.number <= other
        else:
            return NotImplemented

    def __eq__(self, other):
        """等于比较"""
        if isinstance(other, ExcelColumn):
            return self.number == other.number
        elif isinstance(other, int):
            return self.number == other
        elif isinstance(other, str):
            return self.name == other.upper()
        else:
            return False

    def __ne__(self, other):
        """不等于比较"""
        return not self.__eq__(other)

    def __gt__(self, other):
        """大于比较"""
        if isinstance(other, ExcelColumn):
            return self.number > other.number
        elif isinstance(other, int):
            return self.number > other
        else:
            return NotImplemented

    def __ge__(self, other):
        """大于等于比较"""
        if isinstance(other, ExcelColumn):
            return self.number >= other.number
        elif isinstance(other, int):
            return self.number >= other
        else:
            return NotImplemented

    def __repr__(self):
        """对象的官方字符串表示"""
        return f"ExcelColumn('{self.name}')"

    def __str__(self):
        """对象的字符串表示"""
        return self.name


# 使用示例
if __name__ == "__main__":
    # 创建Excel列对象
    a = ExcelColumn("A")
    b = ExcelColumn("B")
    z = ExcelColumn("Z")
    aa = ExcelColumn("aA")

    print(f"A = {a.number}")  # 输出: A = 1
    print(f"B = {b.number}")  # 输出: B = 2
    print(f"Z = {z.number}")  # 输出: Z = 26
    print(f"AA = {aa.number}")  # 输出: AA = 27

    # 加法操作
    print(f"A + B = {a + b}")  # 输出: A + B = C
    print(f"Z + 1 = {z + 1}")  # 输出: Z + 1 = AA

    # 减法操作
    print(f"C - A = {ExcelColumn('C') - a}")  # 输出: C - A = B
    print(f"AA - Z = {aa - z}")  # 输出: AA - Z = A

    # 比较操作
    print(f"A < B: {a < b}")  # 输出: A < B: True
    print(f"Z > AA: {z > aa}")  # 输出: Z > AA: False
    print(f"AA == 27: {aa == 27}")  # 输出: AA == 27: True
    print(f"A == 'a': {a == 'a'}")  # 输出: A == 'a': True
