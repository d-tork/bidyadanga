"""
Turns USB ids into a dataframe and writes it to CSV.

Author: d-tork
Created: 27 Jan 2021
"""
import requests
import pandas as pd
import re


def get_page(url: str) -> requests.Response:
    """Retrieve text from webpage.

    Returns: Response from the GET request

    """
    resp = requests.get(url)
    return resp


def parse_page(resp: requests.Response) -> pd.DataFrame:
    """Parse the page text into dataframe.

    Args:
        resp: Response from GET request.

    Returns: Dataframe of vendor id, vendor, product id, product

    """
    vendor_pattern = r'^(\t?[a-z0-9]{4})\s{2}(.+)$'
    goodlines = re.findall(vendor_pattern, resp.text, flags=re.MULTILINE)
    
    records = []
    for line_id, line_name in goodlines:
        if not line_id.startswith('\t'):
            current_vid = line_id
            current_vendor = line_name
        else:
            pid, product = line_id, line_name
            row = dict(
                vid=current_vid,
                vendor=current_vendor.strip(),
                pid=pid.strip(),
                product=product.strip(),
            )
            records.append(row)
            
    return pd.DataFrame.from_records(records)


def main():
    url = 'http://www.linux-usb.org/usb.ids'
    response = get_page(url=url)
    df = parse_page(resp=response)
    outfile = 'usb_ids.csv'
    df.to_csv(outfile, index=False)

if __name__ == '__main__':
    main()
