WITH unioned_raw_transactions AS (
    SELECT 
        account_number,
        transaction_date,
        posting_date,
        credit_debit,
        category,
        merchant_name,
        amount,
        reference_number,
        transaction_type,
        mcc_code,
        mcc_description
    FROM budget_data.meridian_raw_transactions
)

SELECT 
    am.account_owner ,
    urt.transaction_date,
    urt.posting_date,
    urt.credit_debit,
    urt.category,
    urt.merchant_name,
    urt.amount,
    urt.transaction_type,
    urt.mcc_code,
    urt.mcc_description 
FROM unioned_raw_transactions urt
JOIN budget_data.account_mapping am USING(account_number)