from view.histogramFactory import HistogramFactory
from view.pieFactory import PieFactory
from view.lineChartFactory import LineChartFactory
from view.layoutManager import LayoutManager
from view.CompareBarFactory import CompareBarFactory
from view.CompareLineFactory import CompareLineFactory

# view/view_manager.py
class ViewManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        # Initialisation des usines (Factories)
        self.histogram_maker = HistogramFactory()
        self.pie_maker = PieFactory()
        self.linechart_maker = LineChartFactory()
        self.layout_manager = LayoutManager()
        self.compare_bar_factory = CompareBarFactory()
        self.compare_line_factory = CompareLineFactory()

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
        
    def get_ferrari_layout(self):
        return self.layout_manager.get_ferrari_layout(self.data_manager)
    
    def get_toyota_layout(self):
        return self.layout_manager.get_toyota_layout(self.data_manager)

    def create_histogramme(self, feature, val, active_brand):
        return self.histogram_maker.make_histogram(feature, val, self.data_manager, active_brand)

    def create_pie_chart(self, feature, active_brand):
        return self.pie_maker.make_pie_chart(feature, self.data_manager, active_brand)

    def create_stock_chart(self, active_brand):
        return self.linechart_maker.make_stock_chart(self.data_manager, active_brand)
    
    def create_compare_bar_chart(self, marques, predictions):
        # On demande à l'usine de fabriquer le graphique
        return self.compare_bar_factory.make_compare_bar_chart(marques, predictions)

    def create_compare_line_chart(self, marques):
        # On passe le data_manager à l'usine pour qu'elle puisse lire les CSV
        return self.compare_line_factory.make_compare_line_chart(self.data_manager, marques)
    
    def get_compare_layout(self):
        # On appelle le layout que vous avez défini dans le LayoutManager
        return self.layout_manager.get_compare_layout()