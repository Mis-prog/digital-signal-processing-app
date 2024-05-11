#include "../include/main_lib.h"

int main() {
    SetConsoleOutputCP(CP_UTF8);

    Processing data("data.xlsx");
    data.read_xlsx();
    data.get_index();


    return 0;
}