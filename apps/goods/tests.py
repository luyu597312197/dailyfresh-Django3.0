from django.test import TestCase

# Create your tests here.

class Solution:
    def dailyTemperatures(self, T):
        # 可以维护一个存储下标的单调栈，从栈底到栈顶的下标对应的温度列表中的温度依次递减。
        # 如果一个下标在单调栈里，则表示尚未找到下一次温度更高的下标。
        ans = [0] * len(T)
        stack = []
        for i in range(len(T)):
            while stack and T[stack[-1]] < T[i]:    # 栈不为空 && 栈顶温度小于当前温度
                ans[stack[-1]] = i - stack[-1]
                stack.pop()
            stack.append(i)
        return ans


T = [21,23,24,25,13,12,14]
s = Solution()
b = s.dailyTemperatures(T)
print(b)

