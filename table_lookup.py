# function to find the closest value in a list
def get_closest_value(arr, target):
    n = len(arr)
    left = 0
    right = n - 1
    mid = 0

    # edge case - last or above all
    if target >= arr[n - 1]:
        return arr[n - 1]
    # edge case - first or below all
    if target <= arr[0]:
        return arr[0]
    # BSearch solution: Time & Space: Log(N)

    while left < right:
        mid = (left + right) // 2  # find the mid
        if target < arr[mid]:
            right = mid
        elif target > arr[mid]:
            left = mid + 1
        else:
            return arr[mid]

    if target < arr[mid]:
        return find_closest(arr[mid - 1], arr[mid], target)
    else:
        return find_closest(arr[mid], arr[mid + 1], target)

# findClosest
# We find the closest by taking the difference
# between the target and both values. It assumes
# that val2 is greater than val1 and target lies
# between these two. 
def find_closest(val1, val2, target):
    return val2 if target - val1 >= val2 - target else val1

# function to find index using get_closest_value
# could probably optimise get_closest_value to just return the index, but maybe later
def index_finder(arr, target):
    if target > get_closest_value(arr, target):
         return arr.index(get_closest_value(arr,target))
    else:
        return arr.index(get_closest_value(arr, target))-1