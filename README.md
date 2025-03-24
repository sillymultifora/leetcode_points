# LeetCode Points Progress

This script calculates the estimated date you'll reach your LeetCode points target based on your current points, daily collection habits, and contest participation.

## Usage

```bash
python main.py <current> [target] [--today-collected] [--biweekly-contest] [--weekly-contest] [--weekly-premium]
```

## Arguments

### Required

- **`current`** *(integer)*: Your current number of LeetCode points.

### Optional

- **`target`** *(integer, default: 7200)*: Your target number of points.

## Optional Flags

These flags default to `False`. Specify them in the command line to activate.

- **`--today-collected`**: Indicates today's points have already been collected.
- **`--biweekly-contest`**: Includes points earned from participating in every biweekly contest.
- **`--weekly-contest`**: Includes points earned from participating in every weekly contest.
- **`--weekly-premium`**: Includes points earned by solving premium weekly LeetCode problems.

## Example

To calculate when you'll reach 7200 points from your current 3500 points, assuming you've collected today's points and regularly participate in weekly and biweekly contests:

```bash
python script.py 3500 --today-collected --weekly-contest --biweekly-contest
```

