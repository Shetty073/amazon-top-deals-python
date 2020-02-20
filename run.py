from Crawler import Crawler
import webbrowser

product_name = str(input("Enter the name of the product you are looking for: "))
print("NOTE: Do not use your internet while running this script. It may cause the script to halt prematurely...")
print("NOTE: The top 5 best deals will open in your default web browser automatically once the script finishes executing")
print("<< Ignore any index related errors >>")

craw = Crawler(product_name)
top_five = craw.get_best_deal()
for item in top_five:
    webbrowser.open_new_tab(item["link"])
