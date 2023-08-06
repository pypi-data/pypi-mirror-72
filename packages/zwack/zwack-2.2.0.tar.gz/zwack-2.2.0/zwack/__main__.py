def main():
  import sys
  import zwack
  del sys.argv[0]
  args = sys.argv
  zwack = zwack.Zwack()
  ascii = zwack.ascii()
  try:
    args[0]
  except IndexError:
    print('too little args passed')
    return()
  if(args[0]=='ascii'):
    try:
      piece = args[1]
    except IndexError:
      return
    if(piece=='zwack'):
      print(ascii.zwack)
    elif(piece=='overflow'):
      print(ascii.overflow)
    elif(piece=='overflow_small'):
      print(ascii.overflow_small)
    else:
      print(f'{piece} is not a valid ascii peice')
  else:
    print(f'{args[0]} is not recognised as a command')
if __name__ == '__main__':
  main()