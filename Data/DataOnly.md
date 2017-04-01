# File Hierarchy

* GlobalSettings.py
* Constants.py
* Utilities.py

* UpdateDataCenter.py
  * GetTrading.py
    * Trading.py
  * GetReference.py
    * Reference.py
  * GetClassifying.py
    * Classifying.py
  * GetFundamental.py
    * Fundamental.py
    * FinanceSummary.py
  * GetMacro.py
    * Macro.py
  * GetNewsEvent.py
    * NewsEvent.py
  * GetBillBoard.py
    * BillBoard.py
  * GetShibor.py
    * Shibor.py
  * GetBoxOffice.py
    * BoxOffice.py

* DataOnly.md

# Database Structure

* DataCenter
  * Trading
    * LSHQ
  * Reference
    * RZRQ
      * Reference_RZRQ_Market_SH（沪市融资融券汇总数据）

      * Reference_RZRQ_Market_SZ（深市融资融券汇总数据）

      * Reference_RZRQ_Market_Total（沪深融资融券汇总数据）

      * Reference_RZRQ_Details_SH（沪市融资融券明细数据）

      * Reference_RZRQ_Details_SZ（深市融资融券明细数据）

      * Reference_RZRQ_Details_SH_YYYY-MM-DD（沪市融资融券当天汇总数据）

      * Reference_RZRQ_Details_SZ_YYYY-MM-DD（深市融资融券当天汇总数据）

      * Reference_RZRQ_Details_SH_STOCKID（沪市融资融券个股历史汇总数据）

      * Reference_RZRQ_Details_SZ_STOCKID（深市融资融券个股历史汇总数据）
  * Classifying
    * Industy_Sina
    * Concept_Sina
    * Area
  * Fundamental
    * Basics
    * FinanceSummary
  * Macro
  * NewsEvent
  * BillBoard
  * Shibor
  * BoxOffice