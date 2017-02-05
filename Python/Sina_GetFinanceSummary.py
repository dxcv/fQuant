# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 14:50:27 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
from FinanceSummary import get_finance_summary
import ConstantData as cd

#
# Constants and Parameters
#
stock_ids  = ['300059','600036','000002','002024']

#
# Iteratively Get Finance Summary
#
stock_number = len(stock_ids)
for i in range(stock_number):
    stock_id = stock_ids[i]
    df = get_finance_summary(stock_id)
    # Save to CSV file
    df.to_csv(cd.path_datacenter + cd.file_financesummary % stock_id, encoding='utf-8')
