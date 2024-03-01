from datetime import datetime

# input data is retrieved from Power Automate "Get meeting times" cloud flow via HTTP request

input = %WebServiceResponse%

# sort times
input.sort()

# combine neighboring meeting blocks into one
for i, e in enumerate(input):
    # avoid error on last element
    if i < (len(input) - 1):
        # check if current datetime is the same as the next one
        # print input[i], input[i+1]
        if input[i] == input[i+1]:
            # after the first pop the next element [i+1] becomes the current one [i]
            # we want to remove both duplicates
            input.pop(i)
            input.pop(i)
# print input

output = []

# Combine every two items in array with ' - ' so we can show time span like 8 - 4 pm
for x,y in zip(input[0::2], input[1::2]):
    # convert strings x and y to datetime objects a and b so they can be formatted for human readable output
    a = datetime.strptime(x, '%%Y-%%m-%%dT%%H:%%M:%%S.0000000')
    b = datetime.strptime(y, '%%Y-%%m-%%dT%%H:%%M:%%S.0000000')
    # format list with human readable day of the week, month/day, and times plus time zone
    # dt.strftime("%%A %%m/%%d %%I:%%M%%p %%Z")
    output.append(a.strftime("%%A %%m/%%d %%I:%%M%%p") + ' - ' + b.strftime("%%I:%%M%%p CST"))

print "\n".join(output)
