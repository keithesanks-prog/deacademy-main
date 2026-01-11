import json
import os

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# \ud83d\udd2a Training: Binning Data with `pd.cut()` and `pd.qcut()`\n",
    "## Objective\n",
    "In this lesson, we will learn how to segments and sort data values into bins. This is also called **discretization**.\n",
    "\n",
    "**Key Functions:**\n",
    "- `pd.cut()`: Bin values into discrete intervals.\n",
    "- `pd.qcut()`: Bin values based on sample quantiles (e.g., quartiles)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 1. What is `pd.cut()`?\n",
    "`pd.cut` divides the range of numerical data into bins (intervals). It's useful for converting a continuous variable (like Age or Price) into a categorical one (like Age Group or Price Range).\n",
    "\n",
    "**Syntax:**\n",
    "```python\n",
    "pd.cut(x, bins, labels=None, right=True)\n",
    "```\n",
    "- `x`: The input array/Series to be binned.\n",
    "- `bins`: Integer (number of equal-width bins) or Sequence of scalars (defines the bin edges).\n",
    "- `labels`: Optional labels for the returned bins.\n",
    "- `right`: Boolean, indicates whether bins include the rightmost edge."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2. Example: Creating Age Groups\n",
    "Let's stick to a simple example. We have a list of ages and we want to categorize them into 'Child', 'Teen', 'Adult', 'Senior'."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "\n",
    "df = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],\n",
    "                   'Age': [5, 14, 25, 45, 67, 12]})\n",
    "\n",
    "# Define bin edges: 0-12, 13-19, 20-60, 61-100\n",
    "bins = [0, 12, 19, 60, 100]\n",
    "labels = ['Child', 'Teen', 'Adult', 'Senior']\n",
    "\n",
    "df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)\n",
    "\n",
    "print(\"DataFrame with Age Groups:\")\n",
    "display(df)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 3. Equal-Width Bins\n",
    "If you pass an integer to `bins`, `pd.cut` calculates equal-width bins automatically."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create 3 equal-width bins for Age\n",
    "df['Age_Bin_Equal'] = pd.cut(df['Age'], bins=3)\n",
    "display(df[['Age', 'Age_Bin_Equal']].head())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 4. What is `pd.qcut()`?\n",
    "`pd.qcut` is 'Quantile-based discretization'. It attempts to divide the data into bins that have the **same number of data points**.\n",
    "\n",
    "This is great for creating rankings like 'Top 25%', 'Bottom 25%', etc."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create 3 buckets with roughly equal number of people\n",
    "df['Age_Quantile'] = pd.qcut(df['Age'], q=3, labels=['Young', 'Middle', 'Old'])\n",
    "display(df[['Age', 'Age_Group', 'Age_Quantile']])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Practice Exercise \ud83c\udfcb\ufe0f\u200d\u2640\ufe0f\n",
    "**Problem Statement**\n",
    "You have a DataFrame of student test scores.\n",
    "```python\n",
    "scores_data = {'Student': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],\n",
    "               'Score': [45, 88, 92, 75, 60, 55, 99, 82]}\n",
    "```\n",
    "**Tasks:**\n",
    "1. Create a `Grade` column using `pd.cut` with the following rules:\n",
    "   - 0-59: 'F'\n",
    "   - 60-69: 'D'\n",
    "   - 70-79: 'C'\n",
    "   - 80-89: 'B'\n",
    "   - 90-100: 'A'\n",
    "2. Create a `Performance` column using `pd.qcut` to split students into 4 groups: ['Low', 'Average', 'Good', 'Excellent']."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# --- PRACTICE SOLUTION ---\n",
    "import pandas as pd\n",
    "\n",
    "scores_data = {'Student': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],\n",
    "               'Score': [45, 88, 92, 75, 60, 55, 99, 82]}\n",
    "df_scores = pd.DataFrame(scores_data)\n",
    "\n",
    "# 1. Grades using pd.cut\n",
    "bins = [0, 59, 69, 79, 89, 100]\n",
    "labels = ['F', 'D', 'C', 'B', 'A']\n",
    "df_scores['Grade'] = pd.cut(df_scores['Score'], bins=bins, labels=labels)\n",
    "\n",
    "# 2. Performance using pd.qcut (Quartiles)\n",
    "df_scores['Performance'] = pd.qcut(df_scores['Score'], q=4, labels=['Low', 'Average', 'Good', 'Excellent'])\n",
    "\n",
    "print(\"Practice Results:\")\n",
    "display(df_scores)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open(r'c:\Users\ksank\training\00_Python_Visual_Guides\pandas_cut_lesson.ipynb', 'w') as f:
    json.dump(notebook_content, f, indent=2)
print("Notebook 'pandas_cut_lesson.ipynb' created successfully.")
