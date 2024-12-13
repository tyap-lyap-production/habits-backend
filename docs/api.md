**Habbit**

Name | Type| Require
-- | -- | --
habit_id | UUID | require 
name | string | require
start_date | Date | require
time_of_day | [int enum] | require
area | Area | require
created_date | Date | required
goal_id | Goal | optional
priority | double | required
status_id | Status | optional

---

**Area**

Name | Type| Require
-- | -- | --
area_id | UUID | require 
name | string | require
created_date | Date | required
priority | double | required

---

**Goal**

Name | Type| Require
-- | -- | --
goal_id | UUID | require 
unit_type | int enum | require
value | double | required
periodicity | int enum | required

---

**Status**

Name | Type| Require
-- | -- | --
status_id | UUID | require 
current_value | double | require
target_value | double | required
unit_type | int enum | required
periodicity | int enum | required
reference_date | Date | required

---

**Status**

Name | Type| Require
-- | -- | --
status_id | UUID | require 
current_value | double | require
target_value | double | required
unit_type | int enum | required
periodicity | int enum | required
reference_date | Date | required

---

**User**

Name | Type| Require
-- | -- | --
user_id | UUID | require 
login | string | require
email | string | required
password | string | required