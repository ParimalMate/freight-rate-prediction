# Freight Rate Prediction

Predicts `posted_rate` for 12,000 truckload freight loads in Nov–Dec 2025, trained on 48,000 labelled loads from Jan–Oct 2025.

**Result:** mean absolute error of **$52 (2.2%)** when forecasting two months ahead, measured on three expanding time windows, against **$167** for a naive rate-per-mile baseline.

## Quick start

Python 3.11+ (developed on 3.14), CPU only. A full run takes about 15 minutes.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
brew install libomp        # macOS only: LightGBM needs the OpenMP runtime
python run_all.py          # runs the notebook end to end, writes the predictions and runs score.py
```

`run_all.py` executes `freight_rate_model.ipynb` in place. You can also open the notebook in Jupyter or VS Code and choose **Run All**.

To re-check the submission files on their own:

```bash
python score.py --predictions validation_predictions.csv --december-predictions december-chart-predictions.csv
```

## Outputs

| File | Contents |
|---|---|
| `validation_predictions.csv` | `load_id,predicted_rate` for all 12,000 validation loads |
| `december-chart-predictions.csv` | `december-chart-inputs.csv` with `predicted_rate` filled (the input file is left untouched) |
| `scorer_results/candidate_december.png` | The fixed December chart produced by `score.py` |
| `data_clean/` | Cleaned data, regenerated on every run (not committed) |

## Approach

All of the work is in `freight_rate_model.ipynb`, in six sections:

1. **Exploratory analysis:** rate drivers, data-quality problems, time trends.
2. **Cleaning:** each fix was chosen by comparing alternatives.
   - 677 wrong rates (1.4%) removed using out-of-fold model residuals.
   - Negative weights sign-corrected; capped weights flagged.
   - Missing values filled with methods scored on hidden known values, then re-checked on later months.
   - **`quote_signal` excluded:** in 9 of 10 training months it correlates ±0.99 with the target, and it is noise in Nov–Dec.
3. **Features:** chosen by their effect on time windows. Distance shape, city price levels (8 cities seen only in validation borrow the level of their 5 nearest neighbours), route geometry, calendar, `market_index`. PCA was tested and rejected.
4. **Validation:** expanding windows (Jan–Apr → May–Jun, Jan–Jun → Jul–Aug, Jan–Aug → Sep–Oct). A random split reported less than half the real error.
5. **Models:** Ridge, LightGBM, scikit-learn gradient boosting and a neural network were compared. The final model is a **hybrid**:
   - Ridge (19 features) sets the pricing structure.
   - LightGBM (6 features) corrects Ridge's errors.
   - The overall price level is an equal average of three forecasts: trend, market index, and recent 28-day level.
6. **Predictions and scoring:** writes the files above and runs `score.py`.

## Repository layout

```
freight_rate_model.ipynb              all analysis, modelling and predictions
run_all.py                            runs the notebook end to end
train-test.csv, validation.csv        provided data
validation-predictions-template.csv   provided template
december-chart-inputs.csv             provided December chart inputs
score.py                              provided scorer
```

---

## Original assessment instructions (provided)

See `Freight_Rate_ML_Assessment.pdf` for the assessment instructions.

### What to do

1. Train and validate your model using `data/train_test.csv`.
2. Predict every load in `data/validation.csv`. Each load has a unique `load_id`.
3. Fill the matching `predicted_rate` values in `data/validation_predictions_template.csv` and save it as `validation_predictions.csv`.
4. Predict every row in `data/december_chart_inputs.csv` by filling its `predicted_rate` column.
5. Install the scorer requirements and run:

```bash
python -m pip install -r requirements.txt
python score.py --predictions validation_predictions.csv --december-predictions data/december_chart_inputs.csv
```

The scorer validates both files and creates `scorer_results/candidate_december.png`.

### Submit

- GitHub repository containing your code, dependencies, and run instructions
- `validation_predictions.csv`
- PDF or DOCX report containing your validation, data split approach and `candidate_december.png`
- 2-3 minute Loom link
