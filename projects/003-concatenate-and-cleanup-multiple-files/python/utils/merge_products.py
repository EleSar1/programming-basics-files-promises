from utils.processing import concatenate_data, save_header, clean_data, filter_data
from utils.io_utils import merge_data
from utils.optionals import sort_lines


def main() -> None:
    filenames = ["products_files/products_1.txt", "products_files/products_2.txt", "products_files/products_3.txt"]
    concatenated = concatenate_data(filenames)
    header = save_header(concatenated)
    cleaned = clean_data(concatenated)
    final_data = filter_data(cleaned, header)    
    sorted_data = sort_lines(final_data, 1)

    merge_data("combined_products.txt", header, sorted_data)