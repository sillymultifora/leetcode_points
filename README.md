# 🚀 LeetCode Points Progress 🚀

Tired of manually calculating when you'll finally hit your LeetCode points goal? 🥱 Let this handy script handle the math and predict your victory date! 🏆 Spend less time crunching numbers and more time crushing problems! 🔥

## 🚦 Usage

```bash
python main.py <current> [target] [--today-collected] [--biweekly-contest] [--weekly-contest] [--weekly-premium]
```

## 🎯 Arguments

### ✅ Required

- **`current`** *(integer)*: Your current LeetCode points—show off your progress!

### 🎲 Optional

- **`target`** *(integer, default: 7200)*: Your ultimate LeetCode points goal. Aim high!

## 🚩 Optional Flags

These cool flags default to `False`. Activate them to level-up your prediction!

- **`--today-collected`**: Already grabbed today's points? Let the script know!
- **`--biweekly-contest`**: Adds points for being a biweekly contest regular. Stay consistent!
- **`--weekly-contest`**: Boost your points prediction with weekly contest participation.
- **`--weekly-premium`**: Solve premium weekly LeetCode problems and rake in extra points!

## 🎉 Example

Want to see when you'll celebrate hitting 7200 points, starting from your impressive 3500 points and considering today's progress plus regular contest participation? Easy!

```bash
python main.py 3500 --today-collected --weekly-contest --biweekly-contest
```

Now kick back, relax, and let the script do the math magic. 🎩✨ Less counting, more coding—happy problem-solving! 💻🧠

