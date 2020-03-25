import pandas as pd
import numpy as np

df_input_computation = pd.read_csv("Input_file.csv", encoding='ISO-8859-1', header=0,index_col=0, skip_blank_lines=True)
df_scenarios = pd.read_csv("Simulation_scenarios.csv", encoding='ISO-8859-1',header=0,index_col=0, skip_blank_lines=True)

#parameters
list_indicators = ['cumulative_WGDP%', 'cumulative_GDP%', 'cumulative_FX%', 'cumulative_INF%', 'cumulative_IR%', 'cumulative_External_stock_market%', 'cumulative_Crisis%', 'PD', 'Rating', 'cumulative_default_rate','cumulative_loan_loss_rate', 'cumulative_equity_gain(loss)_rate', 'cumulative_investment_portfolio_gain(loss)_rate','loans', 'loans_gross', 'performing_loans_on_and_off_bs', 'non_performing_loans_gross', 'npl_ratio_gross', 'non_performing_loans_net', 'npl_ratio_net', 'equities', 'equities_fair_value', 'total_loan_exposure_and_equity_valuation', 'cumulative_net_income', 'tra', 'trr', 'total_loan_exposure_and_equity_valuation_base_year', 'loans_base_year', 'performing_loans_on_and_off_bs_base_year', 'equities_fair_value_base_year','equities_base_year']
macro_variables = [ 'WGDP', 'GDP', 'FX', 'INF', 'IR', 'External_stock_market', 'Crisis']

end_year = 2021
base_year = 2018

historical_periods = list(range(int(base_year) - 1, int(base_year) + 1)) 
projection_periods = list(range(int(base_year) + 1, int(end_year) +1))
base_and_projection_periods = list(range(int(base_year)-1, int(end_year) +1))

det_paths = ["1.Corporate - Baseline"]
paths =range(1,1001)

#creating a shell output file for storing simulation results and base year
df_input_computation_base = df_input_computation.copy()
df_input_computation_base.set_index(['Region', 'Region_Mix', 'Country', 'Industry_group', 'Primary_sector', 'Portfolio_manager','Company_name'],inplace=True)

df_indicator_output = []
header_detailed=[]

for i in paths:
    print(i)
    for indicator in list_indicators:
        for x in base_and_projection_periods:
            header = str(i) + '__' + indicator + '__' + str(x)
            header_detailed.append(header)

index_detailed = pd.MultiIndex.from_arrays([df_input_computation.Region, df_input_computation.Region_Mix, df_input_computation.Country, df_input_computation.Industry_group, df_input_computation.Primary_sector, df_input_computation.Portfolio_manager, df_input_computation.Company_name], names=['Region', 'Region_Mix', 'Country', 'Industry Group', 'Primary Sector', 'Portfolio Manager','Company Name'])
df_indicator_output = pd.DataFrame(index=index_detailed, columns=header_detailed, dtype=float).fillna(0)
df_indicator_output.columns = df_indicator_output.columns.astype(str)

df_indicator_output_base = df_input_computation_base.add_prefix(str(-1) + '__')

for x in historical_periods:
    for indicator in list_indicators:
        df_indicator_output[(str(-1) + '__' + indicator + '__' + str(x))] = df_indicator_output_base[(str(-1) + '__' + indicator + '__' + str(x))]

#simulation part which takes several hours
for i in paths: 
    print(i)
    for z in range(0, len(projection_periods)):
        x = projection_periods[z]
        for y in macro_variables:
            df_input_computation[(y + "before_sensitivity__" + str(x))] = df_input_computation.Group.map(df_scenarios[(str(i) + ':' + y + "__" + str(x))]).fillna(0)
            df_input_computation[(y + '__' + str(x))] = np.where((df_input_computation['Sensitivity']==0) | (df_input_computation[det_paths[0] + (':' + y + '_sensitivity' + '__' + str(x))].isnull()), df_input_computation[(y + "before_sensitivity__" + str(x))], np.where(df_input_computation['Sensitivity_type']=="Level", df_input_computation[(det_paths[0] + ':' + y + '_sensitivity' + '__' + str(x))].fillna(0)/100 , df_input_computation[(y + 'before_sensitivity__' + str(x))] + df_input_computation[(det_paths[0] + ':' + y + '_sensitivity' + '__' + str(x))].fillna(0)/100))
        
        df_input_computation[('Crisis' + "__"  + str(x))] = df_input_computation[('Crisis' + "__"  + str(x))]
        df_input_computation[('asset_size' + "__"  + str(x))] = df_input_computation[('asset_size' + "__"  + str(x-1))]
        df_input_computation[('INF' + "__"  + str(x))] = np.where(df_input_computation[('INF' + "__"  + str(x))]<=0, 0.001,df_input_computation[('INF' + "__"  + str(x))])
        df_input_computation[('avg_put_price' + '__' + str(x))] = df_input_computation['avg_put_price']
        df_input_computation[('total_new_commitments_growth_rate' + '__' + str(x))] = df_input_computation['total_new_commitments_growth_rate'] 
        df_input_computation[('total_new_commitments_growth_rate' + '__' + str(x))] = df_input_computation['total_new_commitments_growth_rate'] 
        df_input_computation[('total_new_commitments_growth_rate' + '__' + str(x))] = df_input_computation['total_new_commitments_growth_rate'] 
        df_input_computation[('share_loan_new_commitments_total' + '__' + str(x))] = df_input_computation['share_loan_new_commitments_total'] 
        df_input_computation[('share_equity_new_commitments_total' + '__' + str(x))] = df_input_computation['share_equity_new_commitments_total']
        df_input_computation[('share_guarantee_new_commitments_total' + '__' + str(x))] = df_input_computation['share_guarantee_new_commitments_total']
        df_input_computation[('share_rm_new_commitments_total' + '__' + str(x))] = df_input_computation['share_rm_new_commitments_total']

        df_input_computation[('share_equity_new_commitments' + '__' + str(x))] = df_input_computation['share_loan_new_commitments']
        df_input_computation[('share_loan_new_commitments' + '__' + str(x))] = df_input_computation['share_loan_new_commitments']
        df_input_computation[('share_guarantee_new_commitments' + '__' + str(x))] = df_input_computation['share_loan_new_commitments']
        df_input_computation[('share_rm_new_commitments' + '__' + str(x))] = df_input_computation['share_rm_new_commitments']

        df_input_computation[('loan_commitment_cancellation_rate' + '__' + str(x))] = df_input_computation['loan_commitment_cancellation_rate']
        df_input_computation[('equity_commitment_cancellation_rate' + '__' + str(x))] = df_input_computation['equity_commitment_cancellation_rate']
        df_input_computation[('guarantee_commitment_cancellation_rate' + '__' + str(x))] = df_input_computation['guarantee_commitment_cancellation_rate']
        df_input_computation[('rm_commitment_cancellation_rate' + '__' + str(x))] = df_input_computation['rm_commitment_cancellation_rate']

        df_input_computation[('security_disbursement_rate' + '__' + str(x))] = df_input_computation['security_disbursement_rate']
        df_input_computation[('loan_disbursement_rate' + '__' + str(x))] = df_input_computation['loan_disbursement_rate']
        df_input_computation[('equity_disbursement_rate' + '__' + str(x))] = df_input_computation['equity_disbursement_rate']
        df_input_computation[('guarantee_disbursement_rate' + '__' + str(x))] = df_input_computation['guarantee_disbursement_rate']
        df_input_computation[('rm_disbursement_rate' + '__' + str(x))] = df_input_computation['rm_disbursement_rate']

        df_input_computation[('security_payment_rate' + '__' + str(x))] = df_input_computation['security_payment_rate']
        df_input_computation[('loan_payment_rate' + '__' + str(x))] = df_input_computation['loan_payment_rate']
        df_input_computation[('equity_sale_rate' + '__' + str(x))] = df_input_computation['equity_sale_rate']
        df_input_computation[('guarantee_payment_rate' + '__' + str(x))] = df_input_computation['guarantee_payment_rate']
        df_input_computation[('rm_payment_rate' + '__' + str(x))] = df_input_computation['rm_disbursement_rate']

        df_input_computation[('ear_weight_equities' + '__' + str(x))] = df_input_computation['ear_weight_equities']
        df_input_computation[('ear_weight_loans' + '__' + str(x))] = df_input_computation['ear_weight_loans']
        df_input_computation[('ear_weight_guarantees' + '__' + str(x))] = df_input_computation['ear_weight_guarantees']
        df_input_computation[('ear_weight_rm' + '__' + str(x))] = df_input_computation['ear_weight_rm']

        df_input_computation[('ear_ida_share_loans' + '__' + str(x))] = df_input_computation['ear_ida_share_loans']
        df_input_computation[('ear_ida_share_equities' + '__' + str(x))] = df_input_computation['ear_ida_share_equities']
        df_input_computation[('ear_ida_share_guarantees' + '__' + str(x))] = df_input_computation['ear_ida_share_guarantees']
        df_input_computation[('ear_ida_share_rm' + '__' + str(x))] = df_input_computation['ear_ida_share_rm']

        df_input_computation[('capital_charge_rate_securities' + '__' + str(x))] =df_input_computation['capital_charge_rate_securities']
        df_input_computation[('capital_charge_rate_oprisk' + '__' + str(x))]  = df_input_computation['capital_charge_rate_oprisk']
        df_input_computation[('capital_charge_rate_equities' + '__' + str(x))] =  df_input_computation['capital_charge_rate_equities']
        df_input_computation[('capital_charge_rate_loans' + '__' + str(x))] =  df_input_computation['capital_charge_rate_loans']
        df_input_computation[('capital_charge_rate_guarantees' + '__' + str(x))] =  df_input_computation['capital_charge_rate_guarantees']
        df_input_computation[('capital_charge_rate_rm' + '__' + str(x))] =  df_input_computation['capital_charge_rate_rm']
        df_input_computation[('total_new_commitments' + '__' + str(x))] = df_input_computation[('total_new_commitments' + '__' + str(x-1))]*(1 + df_input_computation[('total_new_commitments_growth_rate' + '__' + str(x))])
        df_input_computation[('loan_new_commitments_total' + '__' + str(x))] = df_input_computation[('total_new_commitments' + '__' + str(x))].sum() * df_input_computation[('share_loan_new_commitments_total' + '__' + str(x))]
        df_input_computation[('equity_new_commitments_total' + '__' + str(x))] = df_input_computation[('total_new_commitments' + '__' + str(x))].sum() * df_input_computation[('share_equity_new_commitments_total' + '__' + str(x))]
        df_input_computation[('guarantee_new_commitments_total' + '__' + str(x))] = df_input_computation[('total_new_commitments' + '__' + str(x))].sum() * df_input_computation[('share_guarantee_new_commitments_total' + '__' + str(x))]
        df_input_computation[('rm_new_commitments_total' + '__' + str(x))] = df_input_computation[('total_new_commitments' + '__' + str(x))].sum() * df_input_computation[('share_rm_new_commitments_total' + '__' + str(x))]

        df_input_computation[('loan_new_commitments' + '__' + str(x))] = df_input_computation[('loan_new_commitments_total' + '__' + str(x))] * df_input_computation[('share_loan_new_commitments' + '__' + str(x))]
        df_input_computation[('equity_new_commitments' + '__' + str(x))] = df_input_computation[('equity_new_commitments_total' + '__' + str(x))] * df_input_computation[('share_equity_new_commitments' + '__' + str(x))]
        df_input_computation[('guarantee_new_commitments' + '__' + str(x))] = df_input_computation[('guarantee_new_commitments_total' + '__' + str(x))] * df_input_computation[('share_guarantee_new_commitments' + '__' + str(x))]
        df_input_computation[('rm_new_commitments' + '__' + str(x))] = df_input_computation[('rm_new_commitments_total' + '__' + str(x))] * df_input_computation[('share_rm_new_commitments' + '__' + str(x))]

        df_input_computation[('loan_commitment_cancellations' + '__' + str(x))] = (df_input_computation[('loan_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('loan_new_commitments' + '__' + str(x))]) * df_input_computation[('loan_commitment_cancellation_rate' + '__' + str(x))] 
        df_input_computation[('equity_commitment_cancellations' + '__' + str(x))] = (df_input_computation[('equity_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('equity_new_commitments' + '__' + str(x))]) * df_input_computation[('equity_commitment_cancellation_rate' + '__' + str(x))] 
        df_input_computation[('guarantee_commitment_cancellations' + '__' + str(x))] = (df_input_computation[('guarantee_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('guarantee_new_commitments' + '__' + str(x))]) * df_input_computation[('guarantee_commitment_cancellation_rate' + '__' + str(x))] 
        df_input_computation[('rm_commitment_cancellations' + '__' + str(x))] = (df_input_computation[('rm_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('rm_new_commitments' + '__' + str(x))]) * df_input_computation[('rm_commitment_cancellation_rate' + '__' + str(x))] 

        df_input_computation[('security_disbursements' + '__' + str(x))] = df_input_computation[('securities' + '__' + str(x-1))]*df_input_computation[('security_disbursement_rate' + '__' + str(x))]
        df_input_computation[('loan_disbursements' + '__' + str(x))] = (df_input_computation[('loan_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('loan_new_commitments' + '__' + str(x))] - df_input_computation[('loan_commitment_cancellations' + '__' + str(x))]) * df_input_computation[('loan_disbursement_rate' + '__' + str(x))] 
        df_input_computation[('equity_disbursements' + '__' + str(x))] = (df_input_computation[('equity_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('equity_new_commitments' + '__' + str(x))] - df_input_computation[('equity_commitment_cancellations' + '__' + str(x))]) * df_input_computation[('equity_disbursement_rate' + '__' + str(x))] 
        df_input_computation[('guarantee_disbursements' + '__' + str(x))] = (df_input_computation[('guarantee_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('guarantee_new_commitments' + '__' + str(x))] - df_input_computation[('guarantee_commitment_cancellations' + '__' + str(x))]) * df_input_computation[('guarantee_disbursement_rate' + '__' + str(x))] 
        df_input_computation[('rm_disbursements' + '__' + str(x))] = (df_input_computation[('rm_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('rm_new_commitments' + '__' + str(x))] - df_input_computation[('rm_commitment_cancellations' + '__' + str(x))]) * df_input_computation[('rm_disbursement_rate' + '__' + str(x))] 

        df_input_computation[('loan_undisbursed_commitments' + '__' + str(x))] = df_input_computation[('loan_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('loan_new_commitments' + '__' + str(x))] - df_input_computation[('loan_commitment_cancellations' + '__' + str(x))] - df_input_computation[('loan_disbursements' + '__' + str(x))]
        df_input_computation[('equity_undisbursed_commitments' + '__' + str(x))] = df_input_computation[('equity_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('equity_new_commitments' + '__' + str(x))] - df_input_computation[('equity_commitment_cancellations' + '__' + str(x))] - df_input_computation[('equity_disbursements' + '__' + str(x))]
        df_input_computation[('guarantee_undisbursed_commitments' + '__' + str(x))] = df_input_computation[('guarantee_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('guarantee_new_commitments' + '__' + str(x))] - df_input_computation[('guarantee_commitment_cancellations' + '__' + str(x))] - df_input_computation[('guarantee_disbursements' + '__' + str(x))]
        df_input_computation[('rm_undisbursed_commitments' + '__' + str(x))] = df_input_computation[('rm_undisbursed_commitments' + '__' + str(x-1))] + df_input_computation[('rm_new_commitments' + '__' + str(x))] - df_input_computation[('rm_commitment_cancellations' + '__' + str(x))] - df_input_computation[('rm_disbursements' + '__' + str(x))]

        df_input_computation[('PD_continous' + '__' + str(x))] = np.maximum(0,np.minimum(1, np.exp(df_input_computation.con_pd + df_input_computation[('PD_log' + '__' + str(x-1))]*df_input_computation.lag_pd + df_input_computation[('GDP' + "__" + str(x))]*df_input_computation.GDP_pd + df_input_computation[('WGDP' + "__" + str(x))]*df_input_computation.WGDP_pd + df_input_computation[('FX' + "__" + str(x))]*df_input_computation.FX_pd))) 
        df_input_computation[('PD_log' + '__' + str(x))] = np.log(df_input_computation[('PD_continous' + '__' + str(x))])
        
        df_input_computation[('Rating' + '__' + str(x))] = np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-6.07, 1.0, np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-5.65,2.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-5.40,3.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-5.15,4.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-4.85,5.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-4.54,6.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-4.23,7.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-3.82,8.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-3.36,9.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-2.86,10.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-2.35,11.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-1.91,12.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-1.30,13.0,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-0.45,14.0,15.0))))))))))))))  
        df_input_computation[('Rating_original' + '__' + str(x))] = df_input_computation[('Rating' + '__' + str(x))]
        df_input_computation[('PD' + '__' + str(x))] = np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-6.07, 0.001775, np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-5.65,0.003025,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-5.40,0.004053,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-5.15,0.005036,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-4.85,0.006625,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-4.54,0.009246,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-4.23,0.012355,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-3.82,0.017256,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-3.36,0.027776,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-2.86,0.043838,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-2.35,0.075482,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-1.91,0.120572,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-1.30,0.183429,np.where(df_input_computation[('PD_log' + '__' + str(x))]<=-0.45,0.404571,1))))))))))))))  

        df_input_computation[('PD_exp' + '__' + str(x))] = np.exp(df_input_computation[('PD_log' + '__' + str(x-1))])

        df_input_computation[('default_rate_before_sensitivity' + '__' + str(x))] = ((df_input_computation.con_dr + df_input_computation[('FX' + "__" + str(x))]*df_input_computation.FX_dr + np.log(df_input_computation[('INF' + "__" + str(x))])*df_input_computation.INF_dr + (df_input_computation[('GDP' + "__" + str(x))] - df_input_computation[('GDP' + "__" + str(x-1))])*df_input_computation.GDP_dr + df_input_computation[('asset_size' + "__" + str(x))]*df_input_computation.Asset_size_dr + df_input_computation[('Crisis' + "__" + str(x))]*df_input_computation.Crisis_dr)*(df_input_computation[('PD_exp' + '__' + str(x))]**(1/3)))**3

        df_input_computation[('default_rate_before_sensitivity' + '__' + str(x))] = np.maximum(0,np.minimum(1, df_input_computation[('default_rate_before_sensitivity' + '__' + str(x))]))

        df_input_computation[('default_rate_after_sensitivity' + '__' + str(x))] =  np.where(((df_input_computation['Sensitivity']==0) |(df_input_computation[det_paths[0] + (':default_rate_sensitivity' + '__' + str(x))].isnull())), df_input_computation[('default_rate_before_sensitivity' + '__' + str(x))], np.where(df_input_computation['Sensitivity_type']=="Level", df_input_computation[det_paths[0] + (':default_rate_sensitivity' + '__' + str(x))].fillna(0)/100 , df_input_computation[('default_rate_before_sensitivity' + '__' + str(x))] + df_input_computation[(det_paths[0] + ':default_rate_sensitivity' + '__' + str(x))]/100))

        df_input_computation[('default_rate' + '__' + str(x))] =   np.maximum(0,np.minimum(1, df_input_computation[('default_rate_after_sensitivity' + '__' + str(x))]))
        df_input_computation[('write_down_rate' + '__' + str(x))] = 0# df_input_computation[('default_rate' + '__' + str(x))]
               
        df_input_computation[('valuation_rate_raw' + '__' + str(x))] = np.minimum(1, np.maximum(-1, .80*(0.05*df_input_computation.mean_ce + df_input_computation.con_ce + df_input_computation[('valuation_rate' + '__' + str(x-1))]*df_input_computation.lag_ce + df_input_computation[('External_stock_market' + "__" + str(x))]*df_input_computation.External_stock_market_ce + df_input_computation[('GDP' + "__" + str(x))]*df_input_computation.GDP_ce + df_input_computation[('FX' + "__" + str(x))]*df_input_computation.FX_ce)))
        df_input_computation[('valuation_rate_before_sensitivity' + '__' + str(x))] = np.minimum(1 + df_input_computation[('write_down_rate' + '__' + str(x))], np.maximum(-1 + df_input_computation[('write_down_rate' + '__' + str(x))], df_input_computation[('valuation_rate_raw' + '__' + str(x))]))
        df_input_computation[('valuation_rate' + '__' + str(x))] = np.where(((df_input_computation['Sensitivity']==0) | (df_input_computation[det_paths[0] + (':valuation_rate_sensitivity' + '__' + str(x))].isnull())), df_input_computation[('valuation_rate_before_sensitivity' + '__' + str(x))], np.where(df_input_computation['Sensitivity_type']=="Level", df_input_computation[det_paths[0] + (':valuation_rate_sensitivity' + '__' + str(x))].fillna(0)/100 , df_input_computation[('valuation_rate_before_sensitivity' + '__' + str(x))] + df_input_computation[(det_paths[0] + ':valuation_rate_sensitivity' + '__' + str(x))]/100))

        df_input_computation[('write_off_rate' + '__' + str(x))] = np.minimum(1, df_input_computation[('write_off_rate')])
    
        df_input_computation[('restructuring_rate' + '__' + str(x))] = np.minimum(1, df_input_computation[('restructuring_rate')])

        df_input_computation[('securities_payment' + '__' + str(x))] = df_input_computation[('securities' + '__' + str(x-1))]*df_input_computation[('security_payment_rate' + '__' + str(x))]
        df_input_computation[('loans_payment' + '__' + str(x))] = df_input_computation[('performing_loans' + '__' + str(x-1))]*df_input_computation[('loan_payment_rate' + '__' + str(x))]*(1 - df_input_computation[('default_rate' + '__' + str(x))])
        df_input_computation[('guarantees_payment' + '__' + str(x))] = df_input_computation[('guarantees' + '__' + str(x-1))]*df_input_computation[('guarantee_payment_rate' + '__' + str(x))]*(1 - df_input_computation[('default_rate' + '__' + str(x))])
        df_input_computation[('rm_payment' + '__' + str(x))] = df_input_computation[('rm' + '__' + str(x-1))]*df_input_computation[('rm_payment_rate' + '__' + str(x))]
        df_input_computation[('equity_sales_valuation' + '__' + str(x))] = df_input_computation[('equities_fair_value' + '__' + str(x-1))]*df_input_computation[('equity_sale_rate' + '__' + str(x))]
        df_input_computation[('general_reserve_rate' + '__' + str(x))] = np.minimum(1, df_input_computation[('general_reserve_rate')])
        df_input_computation[('specific_reserve_rate' + '__' + str(x))] = np.minimum(1,df_input_computation[('specific_reserve_rate')])
        df_input_computation[('LGD' + '__' + str(x))] = df_input_computation[('LGD')]

        df_input_computation[('recovery_rate' + '__' + str(x))] = np.minimum(1,df_input_computation[('recovery_rate')]) #(1-df_input_computation[('restructuring_rate' + '__' + str(x))]-df_input_computation[('LGD' + '__' + str(x))])

        df_input_computation[('borrowings_repayment_rate' + '__' + str(x))] = df_input_computation[('borrowings_repayment_rate')]
        df_input_computation[('borrowings_growth_rate' + '__' + str(x))] = df_input_computation[('borrowings_growth_rate')]

        df_input_computation[('guarantees_to_loans_share' + '__' + str(x))] = df_input_computation[('guarantees_to_loans_share')]

        df_input_computation[('securities_interest_rate' + '__' + str(x))] = df_input_computation[('securities_interest_rate')]
        df_input_computation[('loans_interest_rate' + '__' + str(x))] = df_input_computation[('loans_interest_rate')]
        df_input_computation[('borrowings_interest_rate' + '__' + str(x))] = df_input_computation[('borrowings_interest_rate')]
        df_input_computation[('fee_rate' + '__' + str(x))] =df_input_computation[('fee_rate')]
        df_input_computation[('operating_expense_growth_rate' + '__' + str(x))] = df_input_computation[('operating_expense_growth_rate')]
        df_input_computation[('capital_injection' + '__' + str(x))]= 0

        df_input_computation[('new_borrowings' + '__' + str(x))]=df_input_computation[('borrowings' + '__' + str(x-1))]*df_input_computation[('borrowings_growth_rate' + '__' + str(x))]  
        df_input_computation[('borrowings_repayment' + '__' + str(x))]=df_input_computation[('borrowings' + '__' + str(x-1))]*df_input_computation[('borrowings_repayment_rate' + '__' + str(x))]  

        df_input_computation[('borrowings' + '__' + str(x))] = df_input_computation[('borrowings' + '__' + str(x-1))] + df_input_computation[('new_borrowings' + '__' + str(x))] - df_input_computation[('borrowings_repayment' + '__' + str(x))]
        df_input_computation[('other_assets' + '__' + str(x))] = df_input_computation[('other_assets' + '__' + str(x-1))]
        df_input_computation[('other_liabilities' + '__' + str(x))] = df_input_computation[('other_liabilities' + '__' + str(x-1))]
        df_input_computation[('securities_interest_incomes' + '__' + str(x))] = df_input_computation[('securities' + '__' + str(x-1))]*df_input_computation[('securities_interest_rate' + '__' + str(x))]
        
        df_input_computation[('new_npls' + '__' + str(x))] = df_input_computation[('performing_loans_on_and_off_bs' + '__' + str(x-1))]*df_input_computation[('default_rate' + '__' + str(x))]
        df_input_computation[('call_on_guarantees' + '__' + str(x))] = df_input_computation[('guarantees' + '__' + str(x-1))]*df_input_computation[('default_rate' + '__' + str(x))]
        df_input_computation[('call_on_rm' + '__' + str(x))] = df_input_computation[('rm' + '__' + str(x-1))]*df_input_computation[('default_rate' + '__' + str(x))]
        df_input_computation[('restructured_npls' + '__' + str(x))] = (df_input_computation[('non_performing_loans_net' + '__' + str(x-1))] + df_input_computation[('new_npls' + '__' + str(x))])*df_input_computation[('restructuring_rate' + '__' + str(x))]
        df_input_computation[('loan_write_offs' + '__' + str(x))] = (df_input_computation[('non_performing_loans_net' + '__' + str(x-1))])*df_input_computation[('write_off_rate' + '__' + str(x))]
        df_input_computation[('recovered_npls' + '__' + str(x))] = (df_input_computation[('non_performing_loans_net' + '__' + str(x-1))] + df_input_computation[('new_npls' + '__' + str(x))])*df_input_computation[('recovery_rate' + '__' + str(x))]
        df_input_computation[('performing_loans' + '__' + str(x))] = df_input_computation[('performing_loans' + '__' + str(x-1))] - df_input_computation[('loans_payment' + '__' + str(x))] + df_input_computation[('loan_disbursements' + '__' + str(x))] - df_input_computation[('performing_loans' + '__' + str(x-1))]*df_input_computation[('default_rate' + '__' + str(x))] + df_input_computation[('restructured_npls' + '__' + str(x))] 
        df_input_computation[('guarantees' + '__' + str(x))] =df_input_computation[('guarantees' + '__' + str(x-1))] - df_input_computation[('guarantees_payment' + '__' + str(x))] + df_input_computation[('guarantee_disbursements' + '__' + str(x))] - df_input_computation[('call_on_guarantees' + '__' + str(x))]
        df_input_computation[('rm' + '__' + str(x))] = df_input_computation[('rm' + '__' + str(x-1))] - df_input_computation[('rm_payment' + '__' + str(x))] + df_input_computation[('rm_disbursements' + '__' + str(x))] - df_input_computation[('call_on_rm' + '__' + str(x))]
        df_input_computation[('non_performing_loans_gross' + '__' + str(x))] = df_input_computation[('non_performing_loans_gross' + '__' + str(x-1))] + df_input_computation[('new_npls' + '__' + str(x))]
        df_input_computation[('non_performing_loans_net' + '__' + str(x))] = df_input_computation[('non_performing_loans_net' + '__' + str(x-1))] + df_input_computation[('new_npls' + '__' + str(x))] - df_input_computation[('restructured_npls' + '__' + str(x))] - df_input_computation[('loan_write_offs' + '__' + str(x))]-df_input_computation[('recovered_npls' + '__' + str(x))]
        df_input_computation[('loans' + '__' + str(x))] = df_input_computation[('performing_loans' + '__' + str(x))] + df_input_computation[('non_performing_loans_net' + '__' + str(x))] + df_input_computation[('rm' + '__' + str(x))] + df_input_computation[('guarantees' + '__' + str(x))]
        df_input_computation[('loans_gross' + '__' + str(x))] = df_input_computation[('performing_loans' + '__' + str(x))] + df_input_computation[('non_performing_loans_gross' + '__' + str(x))] + df_input_computation[('rm' + '__' + str(x))] + df_input_computation[('guarantees' + '__' + str(x))]
        df_input_computation[('performing_loans_on_and_off_bs' + '__' + str(x))] = df_input_computation[('performing_loans' + '__' + str(x))] + df_input_computation[('rm' + '__' + str(x))] + df_input_computation[('guarantees' + '__' + str(x))]
        df_input_computation[('specific_reserves' + '__' + str(x))] = df_input_computation[('specific_reserves' + '__' + str(x-1))] + (df_input_computation[('new_npls' + '__' + str(x))] - df_input_computation[('restructured_npls' + '__' + str(x))])*df_input_computation[('LGD' + '__' + str(x))] - df_input_computation[('loan_write_offs' + '__' + str(x))]
        df_input_computation[('general_reserves' + '__' + str(x))] = df_input_computation[('performing_loans_on_and_off_bs' + '__' + str(x))]*df_input_computation[('general_reserve_rate' + '__' + str(x))]
        df_input_computation[('net_loans' + '__' + str(x))] = df_input_computation[('performing_loans' + '__' + str(x))] + df_input_computation[('non_performing_loans_net' + '__' + str(x))] - df_input_computation[('specific_reserves' + '__' + str(x))] - df_input_computation[('general_reserves' + '__' + str(x))]
        df_input_computation[('provisions' + '__' + str(x))] = (df_input_computation[('new_npls' + '__' + str(x))] - df_input_computation[('restructured_npls' + '__' + str(x))])*df_input_computation[('LGD' + '__' + str(x))] + df_input_computation[('general_reserves' + '__' + str(x))] - df_input_computation[('general_reserves' + '__' + str(x-1))]
        df_input_computation[('loans_interest_incomes' + '__' + str(x))] = ((df_input_computation[('performing_loans' + '__' + str(x))] + df_input_computation[('performing_loans' + '__' + str(x-1))])/2)*df_input_computation[('loans_interest_rate' + '__' + str(x))]
        df_input_computation[('borrowings_interest_expenses' + '__' + str(x))] = ((df_input_computation[('borrowings' + '__' + str(x))]+df_input_computation[('borrowings' + '__' + str(x-1))])/2)*df_input_computation[('borrowings_interest_rate' + '__' + str(x))] + df_input_computation[('funding_need' + '__' + str(x-1))]*(df_input_computation[('borrowings_interest_rate' + '__' + str(x))])
        df_input_computation[('fee_incomes' + '__' + str(x))] = ((df_input_computation[('performing_loans' + '__' + str(x))] + df_input_computation[('guarantees' + '__' + str(x))] + df_input_computation[('rm' + '__' + str(x))] + df_input_computation[('performing_loans' + '__' + str(x-1))] + df_input_computation[('guarantees' + '__' + str(x-1))] + df_input_computation[('rm' + '__' + str(x-1))])/2)*df_input_computation[('fee_rate' + '__' + str(x))] 
        df_input_computation[('initial_fundsflow' + '__' + str(x))]=0
        df_input_computation[('final_fundsflow' + '__' + str(x))] = df_input_computation[('initial_fundsflow' + '__' + str(x))] + np.minimum(df_input_computation[('securities' + '__' + str(x-1))]*(1 - df_input_computation[('security_payment_rate' + '__' + str(x))]), np.maximum(-df_input_computation[('initial_fundsflow' + '__' + str(x))],0))
        df_input_computation[('funding_need' + '__' + str(x))] = -np.minimum(df_input_computation[('final_fundsflow' + '__' + str(x))], 0)
        df_input_computation[('available_funding_to_invest' + '__' + str(x))] =  np.maximum(df_input_computation[('final_fundsflow' + '__' + str(x))], 0)
        df_input_computation[('funding_need' + '__' + str(x))].iloc[1:] = 0
        
        df_input_computation[('security_disbursements' + '__' + str(x))] = -np.minimum(df_input_computation[('securities' + '__' + str(x-1))] - df_input_computation[('securities_payment' + '__' + str(x))], np.maximum(-df_input_computation[('initial_fundsflow' + '__' + str(x))],0)) + df_input_computation[('available_funding_to_invest' + '__' + str(x))]
        df_input_computation[('security_disbursements' + '__' + str(x))].iloc[1:] = 0
        df_input_computation[('securities' + '__' + str(x))] = df_input_computation[('securities' + '__' + str(x-1))] - df_input_computation[('securities_payment' + '__' + str(x))] + df_input_computation[('security_disbursements' + '__' + str(x))]  
        df_input_computation[('equity_write_downs_valuation' + '__' + str(x))] = df_input_computation[('equities_fair_value' + '__' + str(x-1))]*df_input_computation[('write_down_rate' + '__' + str(x))]
        df_input_computation[('equity_write_downs_cost' + '__' + str(x))] = df_input_computation[('equities' + '__' + str(x-1))]*df_input_computation[('write_down_rate' + '__' + str(x))]
        df_input_computation[('equity_sales_cost' + '__' + str(x))] = df_input_computation[('equities' + '__' + str(x-1))]*df_input_computation[('equity_sale_rate' + '__' + str(x))]
        df_input_computation[('equities' + '__' + str(x))] = df_input_computation[('equities' + '__' + str(x-1))] + df_input_computation[('equity_disbursements' + '__' + str(x))] - df_input_computation[('equity_write_downs_cost' + '__' + str(x))] - df_input_computation[('equity_sales_cost' + '__' + str(x))]
        df_input_computation[('equity_realized_gains' + '__' + str(x))] = df_input_computation[('ucg' + '__' + str(x-1))]*df_input_computation[('equity_sale_rate' + '__' + str(x))]
        df_input_computation[('equity_fair_valuation_gains(losses)_before_options' + '__' + str(x))] = (df_input_computation[('equities_fair_value' + '__' + str(x-1))] - df_input_computation[('equity_sales_valuation' + '__' + str(x))] - df_input_computation[('equity_write_downs_valuation' + '__' + str(x))])*df_input_computation[('valuation_rate' + '__' + str(x))]
        df_input_computation[('equity_fair_valuation_gains(losses)' + '__' + str(x))] = np.maximum(df_input_computation[('equities' + '__' + str(x))]*df_input_computation[('avg_put_price' + '__' + str(x))]-(df_input_computation[('equities_fair_value' + '__' + str(x-1))]-df_input_computation[('equity_sales_valuation' + '__' + str(x))] - df_input_computation[('equity_write_downs_valuation' + '__' + str(x))]), df_input_computation[('equity_fair_valuation_gains(losses)_before_options' + '__' + str(x))])
        df_input_computation[('equities_fair_value' + '__' + str(x))] = df_input_computation[('equities_fair_value' + '__' + str(x-1))] + df_input_computation[('equity_fair_valuation_gains(losses)' + '__' + str(x))]
        df_input_computation[('ucg' + '__' + str(x))] = df_input_computation[('equities_fair_value' + '__' + str(x))] - df_input_computation[('equities' + '__' + str(x))]
        df_input_computation[('equity_gains(losses)' + '__' + str(x))] =  df_input_computation[('ucg' + '__' + str(x))] - df_input_computation[('ucg' + '__' + str(x-1))] - df_input_computation[('equity_write_downs_cost' + '__' + str(x))]

        df_input_computation[('operating_expenses' + '__' + str(x))] = df_input_computation[('operating_expenses' + '__' + str(x-1))]*(1 + df_input_computation[('operating_expense_growth_rate' + '__' + str(x))]) 
        df_input_computation[('other_incomes_expenses' + '__' + str(x))] = df_input_computation[('other_incomes_expenses' + '__' + str(x-1))] 
        df_input_computation[('net_income_before_ida' + str(x))] = df_input_computation[('securities_interest_incomes' + '__' + str(x))] + df_input_computation[('loans_interest_incomes' + '__' + str(x))] - df_input_computation[('borrowings_interest_expenses' + '__' + str(x))] + df_input_computation[('fee_incomes' + '__' + str(x))] + df_input_computation[('other_incomes_expenses' + '__' + str(x))] + df_input_computation[('equity_gains(losses)' + '__' + str(x))] - df_input_computation[('provisions' + '__' + str(x))] - df_input_computation[('operating_expenses' + '__' + str(x))] 
        df_input_computation[('ida' + '__' + str(x))] = np.where(df_input_computation[('net_income_before_ida' + str(x))]<350,0, df_input_computation[('net_income_before_ida' + str(x))]*0.2727)
        df_input_computation[('net_income' + '__' + str(x))] = df_input_computation[('net_income_before_ida' + str(x))] - df_input_computation[('ida' + '__' + str(x))]
        df_input_computation[('equity' + '__' + str(x))] = df_input_computation[('equity' + '__' + str(x-1))] + df_input_computation[('net_income' + '__' + str(x))] + df_input_computation[('capital_injection' + '__' + str(x))]
        df_input_computation[('total_liabilities_and_equity' + '__' + str(x))] = df_input_computation[('borrowings' + '__' + str(x))] + df_input_computation[('funding_need' + '__' + str(x))] + df_input_computation[('other_liabilities' + '__' + str(x))] + df_input_computation[('equity' + '__' + str(x))]
        df_input_computation[('total_assets' + '__' + str(x))] = df_input_computation[('securities' + '__' + str(x))] + df_input_computation[('equities_fair_value' + '__' + str(x))] + df_input_computation[('net_loans' + '__' + str(x))] + df_input_computation[('other_assets' + '__' + str(x))]

        df_input_computation[('balancing' + '__' + str(x))] = df_input_computation[('total_liabilities_and_equity' + '__' + str(x))] - df_input_computation[('total_assets' + '__' + str(x))]

        df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x))] = df_input_computation[('loans' + '__' + str(x))] + df_input_computation[('equities_fair_value' + '__' + str(x))]

        df_input_computation[('total_loan_exposure_and_equity_valuation_base_year' + '__' + str(x))] = df_input_computation[('total_loan_exposure_and_equity_valuation_base_year' + '__' + str(x-1))]
        df_input_computation[('loans_base_year' + '__' + str(x))] = df_input_computation[('loans_base_year' + '__' + str(x-1))] 
        df_input_computation[('equities_fair_value_base_year' + '__' + str(x))] = df_input_computation[('equities_fair_value_base_year' + '__' + str(x-1))]
        df_input_computation[('equities_base_year' + '__' + str(x))] = df_input_computation[('equities_base_year' + '__' + str(x-1))]
        df_input_computation[('performing_loans_on_and_off_bs_base_year' + '__' + str(x))] = df_input_computation[('performing_loans_on_and_off_bs_base_year' + '__' + str(x-1))]

        df_input_computation[('ear_equities' + '__' + str(x))] = (df_input_computation[('equities_fair_value' + '__' + str(x))] + df_input_computation[('equity_undisbursed_commitments' + '__' + str(x))]*.75) * df_input_computation[('ear_weight_equities' + '__' + str(x))]
        df_input_computation[('ear_loans' + '__' + str(x))] = (df_input_computation[('loans' + '__' + str(x))] + df_input_computation[('loan_undisbursed_commitments' + '__' + str(x))]*.75) * df_input_computation[('ear_weight_loans' + '__' + str(x))]
        df_input_computation[('ear_guarantees' + '__' + str(x))] = (df_input_computation[('guarantees' + '__' + str(x))] + df_input_computation[('guarantee_undisbursed_commitments' + '__' + str(x))]*.75) * df_input_computation[('ear_weight_guarantees' + '__' + str(x))]
        df_input_computation[('ear_rm' + '__' + str(x))] = (df_input_computation[('rm' + '__' + str(x))] + df_input_computation[('rm_undisbursed_commitments' + '__' + str(x))]*.75) * df_input_computation[('ear_weight_rm' + '__' + str(x))]

        df_input_computation[('ear_ida_equities' + '__' + str(x))] = df_input_computation[('ear_equities' + '__' + str(x))] * df_input_computation[('ear_ida_share_equities' + '__' + str(x))]
        df_input_computation[('ear_ida_loans' + '__' + str(x))] = df_input_computation[('ear_loans' + '__' + str(x))] * df_input_computation[('ear_ida_share_loans' + '__' + str(x))]
        df_input_computation[('ear_ida_guarantees' + '__' + str(x))] = df_input_computation[('ear_guarantees' + '__' + str(x))] * df_input_computation[('ear_ida_share_guarantees' + '__' + str(x))]
        df_input_computation[('ear_ida_rm' + '__' + str(x))] = df_input_computation[('ear_rm' + '__' + str(x))] * df_input_computation[('ear_ida_share_rm' + '__' + str(x))]

        df_input_computation[('capital_charge_equities' + '__' + str(x))] = df_input_computation[('capital_charge_rate_equities' + '__' + str(x))] * df_input_computation[('ear_equities' + '__' + str(x))]
        df_input_computation[('capital_charge_loans' + '__' + str(x))] = df_input_computation[('capital_charge_rate_loans' + '__' + str(x))] * df_input_computation[('ear_loans' + '__' + str(x))]
        df_input_computation[('capital_charge_guarantees' + '__' + str(x))] = df_input_computation[('capital_charge_rate_guarantees' + '__' + str(x))] * df_input_computation[('ear_guarantees' + '__' + str(x))]
        df_input_computation[('capital_charge_rm' + '__' + str(x))] = df_input_computation[('capital_charge_rate_rm' + '__' + str(x))] * df_input_computation[('ear_rm' + '__' + str(x))]
        df_input_computation[('ear_oprisk' + '__' + str(x))] = np.maximum(0, df_input_computation[('securities_interest_incomes' + '__' + str(x))].sum() + df_input_computation[('loans_interest_incomes' + '__' + str(x))].sum() + df_input_computation[('equity_gains(losses)' + '__' + str(x))].sum() + df_input_computation[('fee_incomes' + '__' + str(x))].sum()- df_input_computation[('borrowings_interest_expenses' + '__' + str(x))].sum() + df_input_computation[('securities_interest_incomes' + '__' + str(x-1))].sum() + df_input_computation[('loans_interest_incomes' + '__' + str(x-1))].sum() + df_input_computation[('equity_gains(losses)' + '__' + str(x-1))].sum() + df_input_computation[('fee_incomes' + '__' + str(x-1))].sum()- df_input_computation[('borrowings_interest_expenses' + '__' + str(x-1))].sum())

        df_input_computation[('ida_capital_charge_equities' + '__' + str(x))] = np.where(df_input_computation[('ear_ida_equities' + '__' + str(x))].sum()==0, 0, np.maximum(df_input_computation[('ear_ida_equities' + '__' + str(x))].sum() - df_input_computation[('ear_equities' + '__' + str(x))].sum()*0.16,0)*df_input_computation[('capital_charge_rate_equities' + '__' + str(x))].mean()*.25*(df_input_computation[('ear_ida_equities' + '__' + str(x))]/df_input_computation[('ear_ida_equities' + '__' + str(x))].sum()))
        df_input_computation[('ida_capital_charge_loans' + '__' + str(x))] =  np.where(df_input_computation[('ear_ida_loans' + '__' + str(x))].sum()==0, 0, np.maximum(df_input_computation[('ear_ida_loans' + '__' + str(x))].sum() - df_input_computation[('ear_loans' + '__' + str(x))].sum()*0.16,0)*df_input_computation[('capital_charge_rate_loans' + '__' + str(x))].mean()*.25*(df_input_computation[('ear_ida_loans' + '__' + str(x))]/df_input_computation[('ear_ida_loans' + '__' + str(x))].sum()))
        df_input_computation[('ida_capital_charge_guarantees' + '__' + str(x))] = np.where(df_input_computation[('ear_ida_guarantees' + '__' + str(x))].sum()==0,0, np.maximum(df_input_computation[('ear_ida_guarantees' + '__' + str(x))].sum() - df_input_computation[('ear_guarantees' + '__' + str(x))].sum()*0.16,0)*df_input_computation[('capital_charge_rate_guarantees' + '__' + str(x))].mean()*.25*(df_input_computation[('ear_ida_guarantees' + '__' + str(x))]/df_input_computation[('ear_ida_guarantees' + '__' + str(x))].sum()))
        df_input_computation[('ida_capital_charge_rm' + '__' + str(x))] =  np.where(df_input_computation[('ear_ida_rm' + '__' + str(x))].sum()==0,0, np.maximum(df_input_computation[('ear_ida_rm' + '__' + str(x))].sum() - df_input_computation[('ear_rm' + '__' + str(x))].sum()*0.16,0)*df_input_computation[('capital_charge_rate_rm' + '__' + str(x))].mean()*.25*(df_input_computation[('ear_ida_rm' + '__' + str(x))]/df_input_computation[('ear_ida_rm' + '__' + str(x))].sum()))
        df_input_computation[('total_capital_charge_invrisk' + '__' + str(x))] = df_input_computation[('capital_charge_equities' + '__' + str(x))] + df_input_computation[('capital_charge_loans' + '__' + str(x))] + df_input_computation[('capital_charge_guarantees' + '__' + str(x))] + df_input_computation[('capital_charge_rm' + '__' + str(x))] + df_input_computation[('ida_capital_charge_equities' + '__' + str(x))] + df_input_computation[('ida_capital_charge_loans' + '__' + str(x))] + df_input_computation[('ida_capital_charge_guarantees' + '__' + str(x))] +df_input_computation[('ida_capital_charge_rm' + '__' + str(x))]

        df_input_computation[('tra' + '__' + str(x))] = df_input_computation[('tra' + '__' + str(x-1))].sum() + df_input_computation[('net_income' + '__' + str(x))].sum() + (df_input_computation[('specific_reserves' + '__' + str(x))].sum() - df_input_computation[('specific_reserves' + '__' + str(x-1))].sum() + df_input_computation[('general_reserves' + '__' + str(x))].sum() - df_input_computation[('general_reserves' + '__' + str(x-1))].sum()) + df_input_computation[('capital_injection' + '__' + str(x))].sum()
        df_input_computation[('tra' + '__' + str(x))].iloc[1:] = 0

        df_input_computation[('capital_charge_oprisk' + '__' + str(x))] =  np.where(df_input_computation[('total_capital_charge_invrisk' + '__' + str(x))].sum()==0,0,(df_input_computation[('ear_oprisk' + '__' + str(x))]*df_input_computation[('capital_charge_rate_oprisk' + '__' + str(x))])*(df_input_computation[('total_capital_charge_invrisk' + '__' + str(x))]/df_input_computation[('total_capital_charge_invrisk' + '__' + str(x))].sum()))
        
        df_input_computation[('capital_charge_securities' + '__' + str(x))] = np.where(df_input_computation[('total_capital_charge_invrisk' + '__' + str(x))].sum()==0,0,np.maximum(0, 0.10*df_input_computation[('tra' + '__' + str(x))].sum())*(df_input_computation[('total_capital_charge_invrisk' + '__' + str(x))]/df_input_computation[('total_capital_charge_invrisk' + '__' + str(x))].sum()))

        df_input_computation[('total_capital_charge' + '__' + str(x))] = df_input_computation[('capital_charge_oprisk' + '__' + str(x))] + df_input_computation[('capital_charge_securities' + '__' + str(x))] + df_input_computation[('total_capital_charge_invrisk' + '__' + str(x))]

        df_input_computation[('trr' + '__' + str(x))] =  df_input_computation[('trr' + '__' + str(x-1))].sum() + (df_input_computation[('total_capital_charge' + '__' + str(x))].sum() - df_input_computation[('total_capital_charge' + '__' + str(x-1))].sum())
        df_input_computation[('trr' + '__' + str(x))].iloc[1:] = 0
        df_input_computation[('buffer' + '__' + str(x))] = df_input_computation[('tra' + '__' + str(x))]*.10

        df_input_computation[('FX%1' + '__' + str(x))] = df_input_computation[('FX' + '__' + str(x))]
        df_input_computation[('INF%1' + '__' + str(x))] = df_input_computation[('INF' + '__' + str(x))]
        df_input_computation[('IR%1' + '__' + str(x))] = df_input_computation[('IR' + '__' + str(x))]
        df_input_computation[('GDP%1' + '__' + str(x))] = df_input_computation[('GDP' + '__' + str(x))]
        df_input_computation[('WGDP%1' + '__' + str(x))] = df_input_computation[('WGDP' + '__' + str(x))]
        df_input_computation[('External_stock_market%1' + '__' + str(x))] = df_input_computation[('External_stock_market' + '__' + str(x))]
        df_input_computation[('Crisis%1' + '__' + str(x))] = df_input_computation[('Crisis' + '__' + str(x))]
        
        df_input_computation[('growth_rate_of_investment_portfolio1' + '__' + str(x))] = np.where(df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))] ==0,0, (df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x))]/df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))])-1)
        df_input_computation[('growth_rate_of_loans1' + '__' + str(x))] = np.where(df_input_computation[('loans' + '__' + str(x-1))] ==0,0, (df_input_computation[('loans' + '__' + str(x))]/df_input_computation[('loans' + '__' + str(x-1))])-1)
        df_input_computation[('growth_rate_of_equities1' + '__' + str(x))] = np.where(df_input_computation[('equities' + '__' + str(x-1))] ==0,0, (df_input_computation[('equities' + '__' + str(x))]/df_input_computation[('equities' + '__' + str(x-1))])-1)
        df_input_computation[('dsc_ratio1' + '__' + str(x))] =np.where(df_input_computation[('tra' + '__' + str(x))]==0, 0, (df_input_computation[('tra' + '__' + str(x))]-df_input_computation[('trr' + '__' + str(x))] - df_input_computation[('buffer' + '__' + str(x))])/df_input_computation[('tra' + '__' + str(x))])
        df_input_computation[('npl_ratio_gross1' + '__' + str(x))] = np.where(df_input_computation[('loans_gross' + '__' + str(x))]==0, 0, df_input_computation[('non_performing_loans_gross' + '__' + str(x))]/df_input_computation[('loans_gross' + '__' + str(x))])
        df_input_computation[('npl_ratio_net1' + '__' + str(x))] = np.where(df_input_computation[('loans' + '__' + str(x))]==0, 0, df_input_computation[('non_performing_loans_net' + '__' + str(x))]/df_input_computation[('loans' + '__' + str(x))])
        df_input_computation[('default_rate1' + '__' + str(x))] = df_input_computation[('default_rate' + '__' + str(x))]
        df_input_computation[('PD1' + '__' + str(x))] = df_input_computation[('PD' + '__' + str(x))]
        df_input_computation[('Rating1' + '__' + str(x))] = df_input_computation[('Rating' + '__' + str(x))]
        df_input_computation[('loan_loss_rate1' + '__' + str(x))]  = np.where(df_input_computation[('loans' + '__' + str(x-1))]==0, 0, df_input_computation[('provisions' + '__' + str(x))]/df_input_computation[('loans' + '__' + str(x-1))])
        df_input_computation[('equity_gain(loss)_rate1' + '__' + str(x))] = np.where((df_input_computation[('equities_fair_value' + '__' + str(x-1))])==0, 0, df_input_computation[('equity_gains(losses)' + '__' + str(x))]/(df_input_computation[('equities_fair_value' + '__' + str(x-1))]))
        df_input_computation[('investment_portfolio_gain(loss)_rate1' + '__' + str(x))] = np.where((df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))])==0, 0, (df_input_computation[('equity_gains(losses)' + '__' + str(x))] + df_input_computation[('provisions' + '__' + str(x))])/(df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))]))

        df_input_computation[('cumulative_GDP%1' + '__' + str(x))] = df_input_computation[('cumulative_GDP%1' + '__' + str(x-1))]*(1 + df_input_computation[('GDP%1' + '__' + str(x))])
        df_input_computation[('cumulative_FX%1' + '__' + str(x))] = df_input_computation[('cumulative_FX%1' + '__' + str(x-1))]*(1 + df_input_computation[('FX%1' + '__' + str(x))])
        df_input_computation[('cumulative_INF%1' + '__' + str(x))] = df_input_computation[('cumulative_INF%1' + '__' + str(x-1))]*(1 + df_input_computation[('INF%1' + '__' + str(x))])
        df_input_computation[('cumulative_IR%1' + '__' + str(x))] = df_input_computation[('cumulative_IR%1' + '__' + str(x-1))]*(1 + df_input_computation[('IR%1' + '__' + str(x))])
        df_input_computation[('cumulative_WGDP%1' + '__' + str(x))] = df_input_computation[('cumulative_WGDP%1' + '__' + str(x-1))]*(1 + df_input_computation[('WGDP%1' + '__' + str(x))])
        df_input_computation[('cumulative_External_stock_market%1' + '__' + str(x))] = df_input_computation[('cumulative_External_stock_market%1' + '__' + str(x-1))]*(1 + df_input_computation[('External_stock_market%1' + '__' + str(x))])
        df_input_computation[('cumulative_Crisis%1' + '__' + str(x))] = df_input_computation[('cumulative_Crisis%1' + '__' + str(x-1))]*(1 + df_input_computation[('Crisis%1' + '__' + str(x))])
        df_input_computation[('cumulative_growth_rate_of_investment_portfolio1' + '__' + str(x))] = df_input_computation[('cumulative_growth_rate_of_investment_portfolio1' + '__' + str(x-1))]*(1 + df_input_computation[('growth_rate_of_investment_portfolio1' + '__' + str(x))]) 
        df_input_computation[('cumulative_growth_rate_of_loans1' + '__' + str(x))] = df_input_computation[('cumulative_growth_rate_of_loans1' + '__' + str(x-1))]*(1 + df_input_computation[('growth_rate_of_loans1' + '__' + str(x))])
        df_input_computation[('cumulative_growth_rate_of_equities1' + '__' + str(x))] = df_input_computation[('cumulative_growth_rate_of_equities1' + '__' + str(x-1))]*(1 + df_input_computation[('growth_rate_of_equities1' + '__' + str(x))])
        df_input_computation[('cumulative_default_rate1' + '__' + str(x))] = df_input_computation[('cumulative_default_rate1' + '__' + str(x-1))]*(1 + df_input_computation[('default_rate1' + '__' + str(x))]) 
        df_input_computation[('cumulative_loan_loss_rate1' + '__' + str(x))]  = df_input_computation[('cumulative_loan_loss_rate1' + '__' + str(x-1))]*(1 + df_input_computation[('loan_loss_rate1' + '__' + str(x))])
        df_input_computation[('cumulative_equity_gain(loss)_rate1' + '__' + str(x))] = df_input_computation[('cumulative_equity_gain(loss)_rate1' + '__' + str(x-1))]*(1 + df_input_computation[('equity_gain(loss)_rate1' + '__' + str(x))])
        df_input_computation[('cumulative_investment_portfolio_gain(loss)_rate1' + '__' + str(x))] = df_input_computation[('cumulative_investment_portfolio_gain(loss)_rate1' + '__' + str(x-1))]*(1 + df_input_computation[('investment_portfolio_gain(loss)_rate1' + '__' + str(x))])

        df_input_computation[('GDP%' + '__' + str(x))] = df_input_computation[('GDP%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))]
        df_input_computation[('FX%' + '__' + str(x))] = df_input_computation[('FX%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))]
        df_input_computation[('INF%' + '__' + str(x))] = df_input_computation[('INF%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))]
        df_input_computation[('IR%' + '__' + str(x))] = df_input_computation[('IR%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))]
        df_input_computation[('WGDP%' + '__' + str(x))] = df_input_computation[('WGDP%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))]
        df_input_computation[('External_stock_market%' + '__' + str(x))] = df_input_computation[('External_stock_market%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))]
        df_input_computation[('Crisis%' + '__' + str(x))] = df_input_computation[('Crisis%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))]
        df_input_computation[('growth_rate_of_investment_portfolio' + '__' + str(x))] = df_input_computation[('growth_rate_of_investment_portfolio1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))]
        df_input_computation[('growth_rate_of_loans' + '__' + str(x))] = df_input_computation[('growth_rate_of_loans1' + '__' + str(x))]*df_input_computation[('loans' + '__' + str(x-1))]
        df_input_computation[('growth_rate_of_equities' + '__' + str(x))] = df_input_computation[('growth_rate_of_equities1' + '__' + str(x))]*df_input_computation[('equities' + '__' + str(x-1))]
        df_input_computation[('dsc_ratio' + '__' + str(x))] = df_input_computation[('dsc_ratio1' + '__' + str(x))]*df_input_computation[('tra' + '__' + str(x))]
        df_input_computation[('npl_ratio_gross' + '__' + str(x))] = df_input_computation[('npl_ratio_gross1' + '__' + str(x))]*df_input_computation[('loans_gross' + '__' + str(x))]
        df_input_computation[('npl_ratio_net' + '__' + str(x))] = df_input_computation[('npl_ratio_net1' + '__' + str(x))]*df_input_computation[('loans' + '__' + str(x))]
        df_input_computation[('default_rate' + '__' + str(x))] = df_input_computation[('default_rate1' + '__' + str(x))]*(df_input_computation[('performing_loans_on_and_off_bs' + '__' + str(x-1))])
        df_input_computation[('PD' + '__' + str(x))] = df_input_computation[('PD1' + '__' + str(x))]*(df_input_computation[('performing_loans_on_and_off_bs' + '__' + str(x))])
        df_input_computation[('Rating' + '__' + str(x))] = df_input_computation[('Rating1' + '__' + str(x))]*(df_input_computation[('performing_loans_on_and_off_bs' + '__' + str(x))])
        df_input_computation[('loan_loss_rate' + '__' + str(x))]  = df_input_computation[('loan_loss_rate1' + '__' + str(x))]*df_input_computation[('performing_loans_on_and_off_bs' + '__' + str(x-1))]
        df_input_computation[('equity_gain(loss)_rate' + '__' + str(x))] =df_input_computation[('equity_gain(loss)_rate1' + '__' + str(x))]*df_input_computation[('equities_fair_value' + '__' + str(x-1))]
        df_input_computation[('investment_portfolio_gain(loss)_rate' + '__' + str(x))]= df_input_computation[('investment_portfolio_gain(loss)_rate1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation' + '__' + str(x-1))]

        df_input_computation[('cumulative_GDP%' + '__' + str(x))] = df_input_computation[('cumulative_GDP%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_FX%' + '__' + str(x))] = df_input_computation[('cumulative_FX%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_INF%' + '__' + str(x))] = df_input_computation[('cumulative_INF%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_IR%' + '__' + str(x))] = df_input_computation[('cumulative_IR%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_WGDP%' + '__' + str(x))] = df_input_computation[('cumulative_WGDP%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_External_stock_market%' + '__' + str(x))] = df_input_computation[('cumulative_External_stock_market%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_Crisis%' + '__' + str(x))] = df_input_computation[('cumulative_Crisis%1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_growth_rate_of_investment_portfolio' + '__' + str(x))] = df_input_computation[('cumulative_growth_rate_of_investment_portfolio1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_growth_rate_of_loans' + '__' + str(x))] = df_input_computation[('cumulative_growth_rate_of_loans1' + '__' + str(x))]*df_input_computation[('loans_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_growth_rate_of_equities' + '__' + str(x))] = df_input_computation[('cumulative_growth_rate_of_equities1' + '__' + str(x))]*df_input_computation[('equities_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_default_rate' + '__' + str(x))] = df_input_computation[('cumulative_default_rate1' + '__' + str(x))]*df_input_computation[('performing_loans_on_and_off_bs_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_loan_loss_rate' + '__' + str(x))]  = df_input_computation[('cumulative_loan_loss_rate1' + '__' + str(x))]*df_input_computation[('performing_loans_on_and_off_bs_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_equity_gain(loss)_rate' + '__' + str(x))] = df_input_computation[('cumulative_equity_gain(loss)_rate1' + '__' + str(x))]*df_input_computation[('equities_fair_value_base_year' + '__' + str(x))]
        df_input_computation[('cumulative_investment_portfolio_gain(loss)_rate' + '__' + str(x))]= df_input_computation[('cumulative_investment_portfolio_gain(loss)_rate1' + '__' + str(x))]*df_input_computation[('total_loan_exposure_and_equity_valuation_base_year' + '__' + str(x))]
        df_input_computation[('probability_metric' + '__' + str(x))] = df_input_computation[('cumulative_investment_portfolio_gain(loss)_rate' + '__' + str(x))]
        df_input_computation[('cumulative_investment_portfolio_gains(losses)' + '__' + str(x))] = df_input_computation[('cumulative_investment_portfolio_gains(losses)' + '__' + str(x-1))] + df_input_computation[('equity_gains(losses)' + '__' + str(x))] - df_input_computation[('provisions' + '__' + str(x))]
        df_input_computation[('cumulative_net_income' + '__' + str(x))]= df_input_computation[('cumulative_net_income' + '__' + str(x-1))] + df_input_computation[('net_income' + '__' + str(x))]
        df_input_computation[('new_npls_cumulative' + '__' + str(x))]= df_input_computation[('new_npls_cumulative' + '__' + str(x-1))] + df_input_computation[('new_npls' + '__' + str(x))]
        df_input_computation[('equity_gains(losses)_cumulative' + '__' + str(x))]= df_input_computation[('equity_gains(losses)_cumulative' + '__' + str(x-1))] + df_input_computation[('equity_gains(losses)' + '__' + str(x))]
        df_input_computation[('expected_loan_loss_cumulative' + '__' + str(x))]= df_input_computation[('expected_loan_loss_cumulative' + '__' + str(x-1))] + df_input_computation[('provisions' + '__' + str(x))]

        df_input_computation_detailed= df_input_computation.copy()
        df_input_computation_detailed.set_index(['Region', 'Region_Mix', 'Country', 'Industry_group', 'Primary_sector', 'Portfolio_manager','Company_name'],inplace=True)
        df_input_computation_detailed = df_input_computation_detailed.add_prefix(str(i) + '__')

        if x == end_year: 
            for indicator in list_indicators:
                df_indicator_output[(str(i) + '__' + indicator + '__' + str(x))] = df_input_computation_detailed[(str(i) + '__' + indicator + '__' + str(x))]
        else:
            pass
df_indicator_output.reset_index(inplace=True)
df_indicator_output.to_pickle('Output.pkl')
