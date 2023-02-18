def generate_green(num):
    interval = 255/num
    for i in range(1,num):
        print("'rgba("+str(int(i*interval))+",255,0,0.6)',")
    print("'rgba(255,255,0,0.6)',")
    for i in range(1,num):
        print("'rgba(255," + str(int(255-i * interval)) + ",0,0.6)',")
    print("'rgba(255,0,0,0.6)',")
if __name__ =="__main__":
    generate_green(30)