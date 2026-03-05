from view.histogramFactory import HistogramFactory
from view.pieFactory import PieFactory
from view.lineChartFactory import LineChartFactory
from view.layoutManager import LayoutManager

# view/view_manager.py
class ViewManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        # Initialisation des usines (Factories)
        self.histogram_maker = HistogramFactory()
        self.pie_maker = PieFactory()
        self.linechart_maker = LineChartFactory()
        self.layout_manager = LayoutManager()

    def get_car_page(self, brand):
        return self.layout_manager.get_brand_layout(self.data_manager, brand)

    def get_root_layout(self):
        return self.layout_manager.get_root_layout()
    
    def get_home_layout(self):
        return self.layout_manager.get_home_layout()

    def get_tesla_layout(self):
        return self.layout_manager.get_tesla_layout(self.data_manager)
    
    def get_BMW_layout(self):
        return self.layout_manager.get_BMW_layout(self.data_manager)
    
    def get_lambo_layout(self):
        return self.layout_manager.get_lambo_layout(self.data_manager)
    
    def get_toyota_layout(self):
        return self.layout_manager.get_toyota_layout(self.data_manager)

    def create_histogramme(self, feature, val):
        return self.histogram_maker.make_histogram(feature, val, self.data_manage, brand_name)

    def create_pie_chart(self, feature):
        return self.pie_maker.make_pie_chart(feature, self.data_manager, brand_name)

    def create_stock_chart(self):
        return self.linechart_maker.make_stock_chart(self.data_manager, brand_name)