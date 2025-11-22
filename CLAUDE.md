# CLAUDE.md - AI Assistant Guide for for_deletion Repository

## Repository Overview

**Repository Name:** for_deletion
**Purpose:** Machine Learning research repository focused on Explainable AI (XAI) techniques for neural network interpretability
**Primary Domain:** Deep Learning, Explainable AI, Feature Attribution
**Development Environment:** Google Colab (Jupyter notebooks)
**Language:** Python 3.11+

This repository contains experimental notebooks for implementing and visualizing PIRO/FACE (Feature Attribution for Classification Explanations) methods on neural network classifiers.

## Repository Structure

```
for_deletion/
├── README.md              # Minimal readme with Google Drive links
├── Basic.ipynb            # Main ML explainability notebook (liver disorder classification)
├── Untitled4.ipynb        # Python version check notebook
├── Untitled6.ipynb        # ML explainability notebook (similar to Basic.ipynb)
└── CLAUDE.md              # This file - AI assistant guide
```

## Codebase Components

### 1. Basic.ipynb & Untitled6.ipynb
**Purpose:** Neural network training and explainability analysis
**Dataset:** Liver disorder dataset (341 samples, 5 features, binary classification)
**Key Functionality:**
- Train MLP classifier using TensorFlow/Keras
- Generate PIRO feature contribution explanations
- Visualize feature attributions with custom bar charts
- Compare ground truth, network predictions, and explainer predictions

**Key Functions:**
- `get_piro_contrib(x_sample, model, return_weighted=False)` - Computes PIRO feature contributions for a given sample
- `plot_bar_contrib(...)` - Creates horizontal bar plots showing feature attributions

### 2. Untitled4.ipynb
**Purpose:** Environment verification
**Functionality:** Simple Python version check

## Technology Stack

### Core Dependencies
- **mlpxai** - Custom library for explainable AI (MyModel, kerasmlp utilities)
- **TensorFlow/Keras** - Neural network framework
- **scikit-learn** - ML utilities, preprocessing, dataset splitting
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **matplotlib** - Visualization

### Key Modules from mlpxai
- `MyModel` - Custom Keras model wrapper
- `hard_sigmoid`, `hard_tanh` - Custom activation functions
- `run_layers` - Layer-wise forward pass
- `get_transposed_ext` - Extended weight transpose operations
- `print_model_structure` - Model architecture visualization

## Development Workflow

### Typical Notebook Execution Flow
1. **Environment Setup** - Import dependencies, configure warnings
2. **Data Loading** - Load dataset (e.g., liver disorder from CSV)
3. **Data Preprocessing** - MinMaxScaler normalization, train/test split
4. **Model Definition** - Define MLP architecture using Keras functional API
5. **Training** - Compile and fit model with Nadam optimizer
6. **Prediction** - Generate predictions on test samples
7. **Explanation** - Compute PIRO contributions for interpretability
8. **Visualization** - Plot feature attributions

### Data Preprocessing Pattern
```python
# Standard preprocessing pipeline
scaler = MinMaxScaler()
X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, shuffle=True, stratify=y
)
y_train_categorical = to_categorical(y_train, num_outputs).astype(np.float32)
```

### Model Architecture Pattern
```python
# Typical MLP architecture for classification
input_layer = Input(shape=(num_inputs,))
hidden_layer = Dense(30, activation='relu')(input_layer)
hidden_layer = Dense(5, activation='relu')(hidden_layer)
output_layer = Dense(num_outputs, activation='linear')(hidden_layer)

model = MyModel(inputs=input_layer, outputs=output_layer)
model.compile(
    optimizer='nadam',
    metrics=['accuracy'],
    loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True)
)
```

## Key Conventions

### Coding Style
- **Imports:** Grouped by category (standard library, third-party, custom modules)
- **Variable Naming:** Snake_case for variables, functions
- **Configuration:** Inline variable definitions (test_size, validation_split, epochs)
- **Random Seeds:** Set using `keras.utils.set_random_seed(1)` for reproducibility

### Notebook Structure
- **Google Colab Integration:** All notebooks have Colab badges for easy opening
- **Cell Organization:** Sequential execution required (cells depend on previous cells)
- **Output Display:** Training progress and predictions printed inline
- **Visualization:** matplotlib figures displayed inline

### Dataset Handling
- **Feature Names:** Preserved through preprocessing using DataFrame columns
- **Target Encoding:** Binary classification uses dichotomization (threshold-based)
- **Stratification:** Always used in train/test split for balanced classes

### Explainability Workflow
1. Train neural network classifier
2. Select test sample for analysis
3. Compute PIRO contributions using `get_piro_contrib()`
4. Extract class-specific contributions (shape: [num_classes, num_features+1])
5. Visualize with `plot_bar_contrib()` showing positive/negative contributions

## Important Technical Details

### PIRO Algorithm
- **Method:** Layer-wise backpropagation of feature contributions
- **Output:** Contribution matrix [num_classes, num_features + 1] (includes bias)
- **Weighting:** Can return weighted contributions (feature value × contribution)
- **Colors:** Blue = positive contribution, Red = negative contribution

### Visualization Parameters
- **Font Size:** Large fonts (35pt) for publication-quality figures
- **Figure Size:** (14.5, 7.5-9) depending on number of features
- **Max Features:** Typically shows top 12 features by absolute contribution
- **Normalization:** Optional L1 normalization of contributions
- **Output Formats:** SVG support for graph export

### Model Training
- **Optimizer:** Nadam (Adam with Nesterov momentum)
- **Loss:** Categorical cross-entropy with logits
- **Epochs:** 70 (typical)
- **Validation Split:** 10%
- **Test Size:** 15%

## AI Assistant Guidelines

### When Working with This Repository

1. **Understand the Context**
   - This is an XAI research repository focused on neural network interpretability
   - Primary goal is explaining model predictions, not maximizing accuracy
   - Notebooks are designed for Google Colab execution

2. **File Modifications**
   - **Basic.ipynb** and **Untitled6.ipynb** are nearly identical (working copies)
   - Changes should be synchronized if updating both
   - Preserve the sequential cell structure (don't break dependencies)

3. **Code Analysis**
   - The `mlpxai` library is external (not in this repo)
   - Focus on the usage patterns and parameter configurations
   - PIRO contributions are the core explainability output

4. **Testing Changes**
   - Notebooks require Google Colab or local Jupyter environment
   - Need access to liver.csv dataset (referenced in notebooks)
   - Random seed is set for reproducibility (results should be deterministic)

5. **Data Paths**
   - Basic.ipynb references: `sample_data/liver.csv`
   - Untitled6.ipynb references: `liver.csv`
   - Initial cell changes directory: `/content/drive/MyDrive/FACE_Test`

### Common Tasks

**Adding a New Dataset:**
1. Update CSV path and delimiter
2. Adjust feature extraction (X, y splitting)
3. Update `num_inputs` and `num_outputs`
4. Modify `dataset_name` for visualization titles
5. Review target encoding (binary vs multiclass)

**Modifying Model Architecture:**
1. Update layer definitions in model creation cells
2. Ensure compatibility with PIRO algorithm (Dense layers)
3. Adjust hyperparameters (epochs, validation_split)
4. Keep `MyModel` wrapper for PIRO compatibility

**Enhancing Visualizations:**
1. Modify `plot_bar_contrib()` function parameters
2. Adjust `font_size`, `figsize`, `max_features`
3. Toggle `normalize`, `reverse_colors`, `show_title`
4. Update `graph_fname` for export paths

**Debugging PIRO Contributions:**
1. Check model layer types (InputLayer, Dropout handled separately)
2. Verify weights extraction: `layer.get_weights()`
3. Ensure `run_layers()` returns PI_list correctly
4. Validate contribution shape: [num_classes, num_features + 1]

### Git Workflow

**Current Branch:** `claude/claude-md-mia3eeo25s54tayi-01NSFn8uMCrwZ9xvVSZVwabr`
**History Pattern:** Commits labeled "Creado con Colab" (created with Colab)

**When Committing:**
- Use descriptive messages beyond "Update file"
- Mention specific changes (e.g., "Add normalization option to PIRO visualization")
- Follow existing pattern if maintaining Colab-based workflow

**When Pushing:**
- Always push to the designated claude/* branch
- Use: `git push -u origin <branch-name>`
- Branch must start with 'claude/' and match session ID

## Dependencies Installation

For local development (outside Colab):

```bash
pip install tensorflow keras scikit-learn pandas numpy matplotlib
pip install mlpxai  # Custom library (may need special installation)
```

For Colab:
- Most dependencies pre-installed
- May need to install mlpxai separately
- Mount Google Drive if using external datasets

## Troubleshooting

### Common Issues

1. **Missing mlpxai library**
   - Check if library is installed: `pip list | grep mlpxai`
   - May require GitHub installation or custom source

2. **Dataset not found**
   - Verify CSV path matches notebook expectations
   - Check if Google Drive is mounted (Colab)
   - Ensure working directory is correct

3. **Shape mismatches in PIRO**
   - Verify test data preprocessing matches training
   - Check categorical encoding for y_test
   - Ensure model architecture uses Dense layers

4. **Visualization errors**
   - Matplotlib backend issues in some environments
   - Font size may need adjustment for different displays
   - Check feature_names length matches contributions

## Research Context

This repository implements the PIRO (Post-hoc Interpretability for Neural Network Classification) or FACE (Feature Attribution for Classification Explanations) method, which:

- Provides sample-level feature attributions for neural network predictions
- Decomposes predictions into individual feature contributions
- Shows both positive (supportive) and negative (opposing) evidence
- Includes bias/intercept term in explanations
- Works by propagating contributions backward through network layers

The liver disorder dataset is used as a case study for binary classification where the task is predicting alcohol consumption levels (drinks per day) dichotomized at threshold of 7.

## References and External Resources

- **Google Drive Links:** See README.md for shared resources
- **Colab Notebooks:** All notebooks have "Open in Colab" badges
- **Dataset:** Liver disorder dataset (341 samples, 5 physiological features)

---

**Last Updated:** 2025-11-22
**Repository Status:** Active research/experimental repository
**Primary Use Case:** XAI method development and visualization
