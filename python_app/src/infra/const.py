FACILITY_MAP = {
    0: "kernel messages",
    1: "user-level messages",
    2: "mail system",
    3: "system daemons",
    4: "security/authorization messages",
    5: "syslogd internal messages",
    6: "line printer subsystem",
    7: "network news subsystem",
    8: "UUCP subsystem",
    9: "clock daemon",
    10: "security/authorization messages",
    11: "FTP daemon",
    12: "NTP subsystem",
    13: "log audit",
    14: "log alert",
    15: "clock daemon (note 2)",
    16: "local0",
    17: "local1",
    18: "local2",
    19: "local3",
    20: "local4",
    21: "local5",
    22: "local6",
    23: "local7",
}


SEVERITY_MAP = {
    0: "Emergency",  # system is unusable
    1: "Alert",  # action must be taken immediately
    2: "Critical",  # critical conditions
    3: "Error",  # error conditions
    4: "Warning",  # warning conditions
    5: "Notice",  # normal but significant condition
    6: "Informational",  # informational messages
    7: "Debug",  # debug-level messages
}
