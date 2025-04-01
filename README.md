# 🚀 LeetCode Points Calculator 🚀

A powerful tool to predict when you'll reach your LeetCode points goal! 🎯

## 📝 Description

This calculator helps you plan your LeetCode journey by predicting when you'll reach your target points. It takes into account various point sources including daily problems, contests, and premium content.

✨ **Note**: For accurate predictions, run the script either:
- After collecting **all** today's points
- Before collecting **any** points for the day (including daily check-in)

⚠️ **Important**: The calculator assumes:
- You'll collect all available points daily
- No points from contest prizes are included
- The predicted date represents the latest possible date achievable through consistent daily problem-solving

## 🚦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/leetcode-calculator.git
cd leetcode-calculator
```

2. Run the script:
```bash
python main.py <current> [target] [streak] [options]
```

## 🎯 Arguments

### ✅ Required Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `current` | integer | Your current LeetCode points |

### 🎲 Optional Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `target` | integer | 7200 | Your target LeetCode points goal |
| `streak` | integer | 0 | Your current daily streak count |

### 🚩 Optional Flags

| Flag | Description |
|------|-------------|
| `--today-collected` | Indicates you've already collected today's points |
| `--biweekly-contest` | Includes points from biweekly contest participation |
| `--weekly-contest` | Includes points from weekly contest participation |
| `--weekly-premium` | Includes points from weekly premium problems |

## 🎉 Examples

### Basic Usage
```bash
python main.py 3500
```

### Advanced Usage
```bash
python main.py 3500 10000 5 --today-collected --weekly-contest --biweekly-contest
```

### Premium User Example
```bash
python main.py 5000 15000 --weekly-premium --weekly-contest
```

## 📊 Point Sources

The calculator considers the following point sources:
- Daily problems
- Daily check-in
- Weekly contests
- Biweekly contests
- Premium weekly problems

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
