//+------------------------------------------------------------------+
//|                                                        STest.mq5 |
//|                                  Copyright 2021, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2021, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"

#include <MQLMySQL.mqh>

//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
string INI;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnStart()
  {
   string Host, User, Password, Database, Socket; // database credentials
   int Port,ClientFlag;
   int DB; // database handler

   INI = TerminalInfoString(TERMINAL_PATH)+"\\MQL5\\Scripts\\DB\\MyConnection.ini";

// reading database credentials from INI file
   Host = ReadIni(INI, "MYSQL", "Host");
   User = ReadIni(INI, "MYSQL", "User");
   Password = ReadIni(INI, "MYSQL", "Password");
   Database = ReadIni(INI, "MYSQL", "Database");
   Port     = (int)StringToInteger(ReadIni(INI, "MYSQL", "Port"));
   Socket   = ReadIni(INI, "MYSQL", "Socket");
   ClientFlag = (int)StringToInteger(ReadIni(INI, "MYSQL", "ClientFlag"));

// Connecting...
   DB = MySqlConnect(Host, User, Password, Database, Port, Socket, ClientFlag);

   if(DB == -1)
     {
      Print("Connection failed! Error: "+MySqlErrorDescription);
     }
   else
     {
      Print("Connected! DBID#",DB);

      datetime start=D'2021.01.01';
      datetime end=D'2022.01.01';

      store_history(DB, PERIOD_H1, start, end);
      store_history(DB, PERIOD_M15, start, end);
      store_history(DB, PERIOD_M1, start, end);

     }
//+------------------------------------------------------------------+
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void store_history(int DB, const ENUM_TIMEFRAMES period, datetime start, datetime end)
  {
   datetime time[];
   double open[];
   double high[];
   double low[];
   double close[];
   double rsi[];
   double ema50[];
   double ema200[];
   double ema800[];
   long volume[];

// Copy basic data
   CopyTime(_Symbol, period, start, end, time);
   CopyOpen(_Symbol, period, start, end, open);
   CopyHigh(_Symbol, period, start, end, high);
   CopyLow(_Symbol, period, start, end, low);
   CopyClose(_Symbol, period, start, end, close);
   CopyTickVolume(_Symbol, period, start, end, volume);

   int count = ArraySize(time);

// Create indicators
   int handle_rsi = iRSI(_Symbol, period, 14, PRICE_CLOSE);
   int handle_ema50 = iMA(_Symbol, period, 50, 0, MODE_EMA, PRICE_CLOSE);
   int handle_ema200 = iMA(_Symbol, period, 200, 0, MODE_EMA, PRICE_CLOSE);
   int handle_ema800 = iMA(_Symbol, period, 800, 0, MODE_EMA, PRICE_CLOSE);

// Copy indicators data
   CopyBuffer(handle_rsi, 0, start, end, rsi);
   CopyBuffer(handle_ema50, 0, start, end, ema50);
   CopyBuffer(handle_ema200, 0, start, end, ema200);
   CopyBuffer(handle_ema800, 0, start, end, ema800);

   int db_period = get_period(period);

   for(int i =0; i<count; i++)
     {
      // Inserting data
      string Query = "INSERT INTO `test_table` (asset, period, datetime, open, high, low, close, rsi, ema50, ema200, ema800, volume) " +
                     "VALUES ('"+_Symbol+"',"+db_period+",'"+TimeToString(time[i])+"',"+open[i]+","+high[i]+","+low[i]+","+close[i]+","+rsi[i]+","+
                     ema50[i]+","+ema200[i]+","+ema800[i]+","+volume[i]+")";

      if(MySqlExecute(DB, Query))
        {
         Print("Succeeded: ", Query);
        }
      else
        {
         Print("Error: ", MySqlErrorDescription);
         Print("Query: ", Query);
        }

     }
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int get_period(ENUM_TIMEFRAMES period)
  {
   switch(period)
     {
      case PERIOD_M1:
         return 1;
         break;

      case PERIOD_M15:
         return 15;
         break;

      case PERIOD_H1:
         return 60;
         break;

      default:
         return 0;
     }
  }
//+------------------------------------------------------------------+
