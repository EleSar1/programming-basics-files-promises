from utils.processing import concatenate_data, save_header, clean_data, delete_incomplete_data
from utils.io_utils import merge_data


def main() -> None:
    filenames = ["products_files/products_1.txt", "products_files/products_2.txt", "products_files/products_3.txt"]
    concatenated = concatenate_data(filenames)
    header = save_header(concatenated)
    cleaned = clean_data(concatenated)
    final_data = delete_incomplete_data(cleaned, header)    

    merge_data("combined_products.txt", header, final_data)
