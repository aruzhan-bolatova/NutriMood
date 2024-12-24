import requests
import json
import pandas as pd

def fetch_all_items(category_id, max_page_size, store_code):
    url = "https://www.traderjoes.com/api/graphql"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    current_page = 1
    all_items = []

    while True:
        query = """
        query SearchProducts($categoryId: String, $currentPage: Int, $pageSize: Int, $storeCode: String, $availability: String = "1", $published: String = "1") {
          products(
            filter: {store_code: {eq: $storeCode}, published: {eq: $published}, availability: {match: $availability}, category_id: {eq: $categoryId}}
            currentPage: $currentPage
            pageSize: $pageSize
          ) {
            items {
              sku
              item_title
              category_hierarchy {
                id
                name
                __typename
              }
              primary_image
              primary_image_meta {
                url
                metadata
                __typename
              }
              sales_size
              sales_uom_description
              price_range {
                minimum_price {
                  final_price {
                    currency
                    value
                    __typename
                  }
                  __typename
                }
                __typename
              }
              retail_price
              fun_tags
              item_characteristics
              __typename
            }
            total_count
            pageInfo: page_info {
              currentPage: current_page
              totalPages: total_pages
              __typename
            }
            aggregations {
              attribute_code
              label
              count
              options {
                label
                value
                count
                __typename
              }
              __typename
            }
            __typename
          }
        }
        """

        variables = {
            "categoryId": category_id,
            "currentPage": current_page,
            "pageSize": max_page_size,
            "storeCode": store_code,
        }

        payload = json.dumps({"query": query, "variables": variables})

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json()

            if 'errors' in data:
                print(f"API Error: {data['errors']}")
                break
            
            items = data['data']['products']['items']
            for item in items:
                item['storeCode'] = str(store_code)  # Convert store code to string
                all_items.append(item)  # Add items to the list
            
            total_pages = data['data']['products']['pageInfo']['totalPages']

            if current_page >= total_pages:
                break
            
            current_page += 1

        except requests.RequestException as e:
            print(f"Error fetching items: {e}")
            break

    return all_items

def save_to_csv(unique_items, filename):
    df = pd.DataFrame(unique_items)

    # Group by item title and aggregate store codes
    df = df.groupby(['item_title']).agg({
        'sku': 'first',  # Keep the first SKU
        'storeCode': lambda x: ', '.join(sorted(set(x))),  # Combine store codes
        'category_hierarchy': 'first',  # Keep the first occurrence
        'primary_image': 'first',
        'primary_image_meta': 'first',
        'sales_size': 'first',
        'sales_uom_description': 'first',
        'price_range': 'first',
        'retail_price': 'first',
        'fun_tags': 'first',
        'item_characteristics': 'first',
    }).reset_index()

    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def load_store_codes_from_csv(csv_file):
    store_df = pd.read_csv(csv_file)
    # Assuming the store number is in the column 'Store Number'
    store_codes = store_df['Store Number'].astype(str).tolist()
    return store_codes

def main():
    category_id = "8"  # Set this to the desired category ID
    max_page_size = 100  # Use the maximum allowed page size
    filename = "trader_joes_items.csv"

    # Load store codes from CSV
    csv_file = 'store_numbers.csv'  # CSV file with store codes
    store_codes = load_store_codes_from_csv(csv_file)

    all_items = []

    for store_code in store_codes:
        print(f"Fetching items for store code: {store_code}")
        items = fetch_all_items(category_id, max_page_size, store_code)
        all_items.extend(items)

    # Use a dictionary to ensure items are unique based on item title
    item_dict = {}

    for item in all_items:
        item_name = item['item_title'].lower()  # Normalize the item title for uniqueness check
        if item_name not in item_dict:
            item_dict[item_name] = item  # Store the first occurrence
            item_dict[item_name]['storeCode'] = str(item['storeCode'])  # Ensure storeCode is a string
        else:
            # Ensure that storeCode is always a string and append it
            existing_store_codes = item_dict[item_name]['storeCode']
            new_store_code = str(item['storeCode'])
            if new_store_code not in existing_store_codes.split(', '):
                item_dict[item_name]['storeCode'] += f", {new_store_code}"  # Append the new store code

    # Convert the dictionary back to a list
    unique_items = list(item_dict.values())

    # Save the results to a CSV file
    save_to_csv(unique_items, filename)

if __name__ == "__main__":
    main()
