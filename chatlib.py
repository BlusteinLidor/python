# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message
CMD_LIST = ["LOGIN", "LOGOUT", "LOGGED", "GET_QUESTION", "SEND_ANSWER"
, "MY_SCORE", "HIGHSCORE", "LOGIN_OK", "LOGGED_ANSWER", "YOUR_QUESTION"
, "CORRECT_ASNWER", "WRONG_ANSWER", "YOUR_SCORE", "ALL_SCORE", "ERROR"
, "NO_QUESTIONS"]

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
	if cmd in CMD_LIST:
		cmd_len = len(cmd)
		if cmd_len < 16:
			cmd = cmd + " "*(16-cmd_len)
		elif cmd_len > 16:
			return None
		data_len = len(data)
		data_len_str = str(data_len).zfill(4)
		full_msg = f"{cmd}|{data_len_str}|{data}"
		return full_msg


def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
	if data.count("|") != 2:
		return None
	else:
		data_list = data.split("|")
		cmd = data_list[0].strip()
		if not cmd in CMD_LIST:
			return None, None
		else:
			msg = data_list[2]
			msg_len = len(msg)
			char_num = data_list[1].lstrip("0")
			char_num = char_num.strip()
			if msg_len != int(char_num):
				return None, None
			else:
				return cmd, msg

	
def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	split_msg = msg.split("#")
	num = 0
	for char in msg:
		if char == "#":
			num += 1
	if num == expected_fields:
		return split_msg
	else:
		return None


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	for element in msg_fields:
		if not isinstance(element, str):
			str_element = str(element)
			element = str_element
	'#'.join(msg_fields)