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
        self.layout_manager = LayoutManager()
        mon_theme = self.layout_manager.theme

        # Initialisation des usines (Factories)
        self.histogram_maker = HistogramFactory(mon_theme)
        self.pie_maker = PieFactory(mon_theme)
        self.linechart_maker = LineChartFactory(mon_theme)
        self.compare_bar_factory = CompareBarFactory(mon_theme)
        self.compare_line_factory = CompareLineFactory(mon_theme)

    def get_car_page(self, brand):
        return self.layout_manager.get_brand_layout(self.data_manager, brand)

    def get_root_layout(self):
        marques = self.data_manager.get_marques()
        return self.layout_manager.get_root_layout(marques)

    def get_home_layout(self):
        return self.layout_manager.get_home_layout(self.data_manager)

    def create_histogramme(self, feature, val, active_brand):
        return self.histogram_maker.make_histogram(
            feature, val, self.data_manager, active_brand
        )

    def create_pie_chart(self, feature, active_brand):
        return self.pie_maker.make_pie_chart(feature, self.data_manager, active_brand)

    def create_stock_chart(self, active_brand, extra_lines=None):
        return self.linechart_maker.make_stock_chart(
            self.data_manager, active_brand, extra_lines=extra_lines
        )

    def create_compare_bar_chart(self, marques, predictions):
        return self.compare_bar_factory.make_compare_bar_chart(
            marques, predictions, self.data_manager
        )

    def create_compare_line_chart(self, marques):
        return self.compare_line_factory.make_compare_line_chart(
            self.data_manager, marques
        )

    def get_compare_layout(self):
        return self.layout_manager.get_compare_layout()

    def get_feature_description(self, feature, brand):
        descriptions = {
            "Open": "Opening price for the day",
            "High": "Highest price reached during the trading session",
            "Low": "Lowest price reached during the session",
            "Close": "Closing price for the day",
            "Volume": "Trading volume (securities traded).",
            "MA_7": "7-day moving average",
        }
        return descriptions.get(feature, f"Analysis of {feature} for {brand}.")
