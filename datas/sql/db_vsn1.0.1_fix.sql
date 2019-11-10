set global log_bin_trust_function_creators = 1;

DROP FUNCTION IF EXISTS currval;
DROP FUNCTION IF EXISTS nextval;


DELIMITER ;;
--
-- 函数
--
CREATE DEFINER=`user_py_admin`@`%` FUNCTION `currval` (`seq_name` VARCHAR(40)) RETURNS INT(11) SQL SECURITY INVOKER
BEGIN
DECLARE ret_value INTEGER;
SET ret_value=0;
SELECT `value` INTO ret_value
FROM `sequence`
WHERE `key`=seq_name;
RETURN ret_value;
END;;

CREATE DEFINER=`user_py_admin`@`%` FUNCTION `nextval` (`seq_name` VARCHAR(40), `incr` INT(11)) RETURNS INT(11) SQL SECURITY INVOKER
BEGIN
    UPDATE `sequence` SET `value` = `value` + incr where `key`=seq_name;

    set @val = currval(seq_name);
    if @val = 0 then
        insert into `sequence` (`key`, `value`) value (seq_name, incr);
        set @val = incr;
    end if;
    return @val;
END;;
