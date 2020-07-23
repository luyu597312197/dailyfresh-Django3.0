from django.test import TestCase

# Create your tests here.

class Fun:
    def dailyTemperatures(self, t):
        ans = [0] * len(t)
        stack = []
        for i in range(len(t)):
            while stack and t[stack[-1]] < t[i]:
                ans[stack[-1]] = i - stack[-1]
                stack.pop()
            stack.append(i)
        return ans

