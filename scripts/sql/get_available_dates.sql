-- Run this in the Supabase SQL Editor so get_available_dates() can query
-- distinct dates server-side (avoids the 1000-row default limit).

CREATE OR REPLACE FUNCTION "NYISO_NYC_Load_Actual_5_Minute".get_available_dates()
RETURNS TABLE (available_date date)
LANGUAGE sql
STABLE
AS $$
  SELECT DISTINCT ("RTD_End_Time_Stamp")::date AS available_date
  FROM "NYISO_NYC_Load_Actual_5_Minute"."June_2026"
  ORDER BY available_date;
$$;

GRANT EXECUTE ON FUNCTION "NYISO_NYC_Load_Actual_5_Minute".get_available_dates()
  TO anon, authenticated, service_role;
