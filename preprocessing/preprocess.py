import argparse
import pandas as pd

def load_and_process_csv(file_path, question_col, answer_col):
    """
    Load the CSV file, select specific columns for question and answer, and rename them.
    """
    try:
        df = pd.read_csv(file_path)
        df = df[[question_col, answer_col]].rename(columns={question_col: 'question', answer_col: 'answer'})
        return df

    except KeyError:
        raise KeyError(f"Columns '{question_col}' or '{answer_col}' not found in {file_path}.")

    except Exception as e:
        raise Exception(f"An error occurred while processing {file_path}: {e}")


def remove_outliers(df, question_col='question'):
    """
    Remove rows where the length of the text in the question column is less than 3 or greater than 25.
    """
    print(f"Removing outliers from {len(df)} rows...")
    df = df[df[question_col].str.len().between(3, 100)]
    print(f"Outliers removed. Remaining rows: {len(df)}")
    return df


def main(open_dataset_path, specific_dataset_path, open_question_col, open_answer_col, specific_question_col, specific_answer_col):
    """
    Load and process two CSV files, one open-domain and one specific-domain, based on provided question and answer columns.
    Perform outlier removal on the question columns of both files.
    """
    # Open-domain CSV
    print(f"Loading and processing {open_dataset_path}...")
    open_df = load_and_process_csv(open_dataset_path, open_question_col, open_answer_col)
    open_df = remove_outliers(open_df)
    print()

    # Specific-domain CSV
    print(f"Loading and processing {specific_dataset_path}...")
    specific_df = load_and_process_csv(specific_dataset_path, specific_question_col, specific_answer_col)
    specific_df = remove_outliers(specific_df)
    print()

    # Label the datasets
    open_df['label'] = 0
    specific_df['label'] = 1

    # Save the preprocessed data
    open_df.to_csv("../data/open_domain_data.csv", index=False)
    specific_df.to_csv("../data/specific_domain_data.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process two datasets with specified question and answer columns.")
    parser.add_argument("open_dataset_path", type=str, help="Path to the open-domain dataset CSV file.")
    parser.add_argument("specific_dataset_path", type=str, help="Path to the specific-domain dataset CSV file.")
    parser.add_argument("open_question_col", type=str, help="Question column name in the open-domain dataset.")
    parser.add_argument("open_answer_col", type=str, help="Answer column name in the open-domain dataset.")
    parser.add_argument("specific_question_col", type=str, help="Question column name in the specific-domain dataset.")
    parser.add_argument("specific_answer_col", type=str, help="Answer column name in the specific-domain dataset.")

    args = parser.parse_args()

    main(
        args.open_dataset_path,
        args.specific_dataset_path,
        args.open_question_col,
        args.open_answer_col,
        args.specific_question_col,
        args.specific_answer_col
    )

    print("Preprocessing completed successfully.")

    # Example usage: python preprocess.py ../data/arxiv.csv ../data/law_domain.csv Question Response title answer