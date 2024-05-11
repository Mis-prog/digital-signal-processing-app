import data as processing_data
import plot as plot_data
import filter as filter_data

data = processing_data.get_data("../data/data.xlsx")
name = 'Data 12'
# plot_data.plot(data[['MD', name]], scatter=False)

border = processing_data.get_index_start_end_work(data, name)
start_ = border[0][0]
end_ = border[0][1]

data_check = processing_data.get_data_by_border(data, start_, end_, name)

data_check = processing_data.get_data_with_frequency(data_check, 2 )
plot_data.plot(data_check, scatter=False)

data_check_filter = filter_data.moving_average_manual_mean(data_check, name, 100)
#
#
data_print=[(name,data_check),(name+' filter',data_check_filter)]
#
plot_data.plot_multiple(data_print,name)