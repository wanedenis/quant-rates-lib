quant-rates-lib/
│
├── README.md
├── pyproject.toml
├── requirements.txt
│
├── quant_rates/
│   ├── __init__.py
│   ├── market/
│   │   ├── yield_curve.py
│   │   └── discounting.py
│   │
│   ├── instruments/
│   │   ├── bond.py
│   │   └── swap.py
│   │
│   ├── pricing/
│   │   └── pricers.py
│   │
│   └── utils/
│       └── day_count.py
│
├── tests/
│   ├── test_bond.py
│   ├── test_curve.py
│   └── test_swap.py
│
└── docs/
    └── design.md
