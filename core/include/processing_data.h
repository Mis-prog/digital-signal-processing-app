#pragma once

#include "../external/OpenXLSX/OpenXLSX/OpenXLSX.hpp"
#include <string>
#include <vector>


struct Data {
    int start_index = 0, end_index = 0;

    std::string name_colums;
    std::vector<std::pair<int, int>> index;
};

class Processing {
private:
    OpenXLSX::XLDocument doc;

    const std::string path = "../../data/";

    std::string name_file;
    std::map<std::string, std::vector<Data>> data; // name_sheet,data
public:
    Processing(std::string name);

    void read_xlsx();

    void write_xlsx();

    std::vector<std::string> get_name_sheet(OpenXLSX::XLDocument &document);

    std::vector<std::string> get_name_columns(std::string name_sheet);

    int get_count_sheet();

    void
    get_index();

    void method_moving_average();

    ~Processing();
};
