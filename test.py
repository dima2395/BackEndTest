


def get_list_of_pages(current_page,
                      ammount_of_pages,
                      pages_to_display = 10,
                      left_max = 5,
                      right_max = 4):
  list_of_pages = []
  if ammount_of_pages > pages_to_display:
    if current_page-1 <= left_max:
      [list_of_pages.append(x) for x in range(1, current_page+1)]
      i = current_page + 1
      while len(list_of_pages) != pages_to_display:
        list_of_pages.append(i)
        i += 1
    else:
      [list_of_pages.append(x) for x in range(current_page-left_max, current_page+1)]
      i = current_page + 1
      while len(list_of_pages) != pages_to_display:
        list_of_pages.append(i)
        i += 1
  # else:
  #   if current_page-1 <= left_max:
  #     [list_of_pages.append(x) for x in range(1, current_page+1)]
  #     i = current_page + 1
  #     while len(list_of_pages) != ammount_of_pages:
  #       list_of_pages.append(i)
  #       i += 1

  return list_of_pages

print(get_list_of_pages(5,12))