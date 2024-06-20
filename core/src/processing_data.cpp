#include "../include/processing_data.h"


Processing::Processing(std::string name) {
    name_file = name;

//    std::cout << name_file << std::endl;
    doc.open(path + name_file);
}

void Processing::read_xlsx() {
    std::vector<std::string> sheet_name = get_name_sheet(doc);

    for (std::string name_: sheet_name) {
        std::vector<Data> curr_sheet;

        std::vector<std::string> columns_name = get_name_columns(name_);
        for (auto name__: columns_name) {
            Data curr_data;
            curr_data.name_colums = name__;

            curr_sheet.push_back(curr_data);
        }
        data[name_] = curr_sheet;
    }

}


Processing::~Processing() {
//    data.clear();
    doc.close();
}

void Processing::write_xlsx() {

}

std::vector<std::string> Processing::get_name_sheet(OpenXLSX::XLDocument &document) {
    std::vector<std::string> name_sheets;

    if (document.isOpen()) {
        for (const auto &sheetName: document.workbook().sheetNames()) {
            name_sheets.push_back(sheetName);
        }
        return name_sheets;
    }
    return std::vector<std::string>();
}

std::vector<std::string> Processing::get_name_columns(std::string name_sheet) {
    std::vector<std::string> name_columns;

    if (doc.isOpen()) {

        auto sheet = doc.workbook().worksheet(name_sheet);

        for (int j = 2; j <= sheet.columnCount(); j++) {
            auto cellValue = sheet.cell(1, j).value().get<std::string>();
            name_columns.push_back(cellValue);
//            std::cout << cellValue << " ";
        }
//        std::cout << std::endl;
        return name_columns;
    }
    return std::vector<std::string>();
}

int Processing::get_count_sheet() {
    if (doc.isOpen()) {
        return doc.workbook().sheetCount();
    } else {
        return 0;
    }
}

void Processing::get_index() {

    auto book = doc.workbook();

    for (auto data_book: data) {
        std::cout << data_book.first << " " << std::endl;

        auto sheet = doc.workbook().worksheet(data_book.first);
        int count_value = sheet.rowCount();

        for (int index_column = 1; index_column <= data_book.second.size(); index_column++) {
            for (int index_value = 2; index_value <= count_value; index_value++) {
                std::cout << sheet.cell(index_v

//                std::cout << sheet.cell(index_value,index_column).value().get<std::float_t>();
            }
        }
    }
}


void Processing::method_moving_average() {

}

void Processing::string_to_value() {
    //split . or ,
    // right + left
}
