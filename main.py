import tkinter as tk
import random
import math
import time

# Shared variable to store max_fit
current_max_fit = None

# number of cities
CT = 5
# number of population
P_SIZE = 100

# max of population, số thế hệ tối đa
max_generation = 13


MIN_COORDINATE = 1
MAX_COORDINATE = 500
START_END_POINT = 0

# init city with coordinate x, y
class City:
    def __init__(self):
        self.x = 0
        self.y = 0
    
# doc file
    # def __init__(self, x, y):
    #     self.x = x
    #     self.y = y

# init individual with gen and fitness
class individual:
    def __init__(self) -> None:
        self.gen = []
        self.fitness = 0
    def __lt__(self, other):
        return self.fitness < other.fitness
    def __gt__(self, other):
        return self.fitness > other.fitness

# random cities coordinate x, y  
def init_cities_coordinate():
    ct = []
    for i in range(CT):
        temp = City()
        flag = 1
        while flag:
            temp.x = random.randint(MIN_COORDINATE, MAX_COORDINATE)
            temp.y = random.randint(MIN_COORDINATE, MAX_COORDINATE)
            if temp not in ct:
                flag = 0
        ct.append(temp)
    return ct

# calculate distance from spot A to spot B
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# dict lưu những cặp thành phố đã được tính khoảng cách
distanceDict = dict()

def calculate_distance(gen):
    f = 0
    for i in range(len(gen) - 1):
        key = (gen[i], gen[i+1])
        key1 = (gen[i+1], gen[i])
        if (key in distanceDict) or (key1 in distanceDict):
            # Cặp khóa (i, j) đã tồn tại trong từ điển
            f += distanceDict.get(key)
        else:
            d = distance(ct_coord[gen[i]].x, ct_coord[gen[i]].y, ct_coord[gen[i+1]].x, ct_coord[gen[i+1]].y)
            distanceDict[key] = d
            distanceDict[key1] = d
            f += d
    return f

def create_population(CT):
    population = [] # quần thể rỗng
    array = list(range(1, CT)) # tạo 1 mảng lưu các thành phố trừ thành phố khởi đầu
    for i in range(P_SIZE):
        temp = individual()
        random.shuffle(array) # xáo trộn thứ tự các thành phố để tạo ra cá thể của quần thể
        temp.gen = [0] + array + [0] # gắn thành phố khởi đầu vào đầu và cuối chuỗi để khép kín thành chu trình
        temp.fitness = 1/calculate_distance(temp.gen)
        population.append(temp) # thêm cá thể vừa tạo vào quần thể
    population.sort(reverse=True) # sắp xếp quần thể theo thứ tự tăng dần của fitness
    return population

def crossover(parent1, parent2):
    
    splitPoint = random.randint(1, CT-2) # tạo điểm cắt

    # loại bỏ 2 điểm 0 ở 2 đầu
    parent1 = list(filter(lambda x: x != 0, parent1))
    parent2 = list(filter(lambda x: x != 0, parent2))
    
    # tạo offspring1 là đoạn sau của gen parent1
    offspring1 = parent1[splitPoint:]

    # xóa các phần tử có trong offspring1 ra khỏi parent 2 để tạo offspring 2
    offspring2 = parent2
    for i in offspring1:
        offspring2.remove(i)

    # trả về chuỗi con vừa tạo được
    offspring = offspring2 + offspring1
    return offspring

# đột biến
def mutate(Gen, mutation_rate):
    mutated_individual = Gen
    if random.random() < mutation_rate:
        i1 = random.randint(0, CT-2) # chọn ngẫu nhiên vị trí đầu tiên
        while True:
            i2 = random.randint(0, CT-2) # chọn ngẫu nhiên ví trí thứ 2 khác vị trí đầu tiên
            if i2 != i1:
                break

        # đổi giá trị của 2 vị trí vừa được chọn
        temp = mutated_individual[i1]
        mutated_individual[i1] = mutated_individual[i2]
        mutated_individual[i2] = temp
    

    return [0] + mutated_individual + [0]


def create_window():
    global finish_time
    global generation



    # Tọa độ các điểm
    city = ct_coord

    # Vẽ các thành phố
    for i in range(CT):
        oval = canvas.create_text(city[i].x, city[i].y, text=i, fill="blue")

    # Vẽ các đường nối
    for i in range(CT):
        line = canvas.create_line(city[current_max_fit.gen[i]].x, city[current_max_fit.gen[i]].y,
                                  city[current_max_fit.gen[i+1]].x, city[current_max_fit.gen[i+1]].y)
    


    canvas.create_text(canvas.winfo_reqwidth() - 10, 10,
                       text=f"Elapsed Time: {finish_time:.2f} seconds", 
                       anchor=tk.NE, fill="green")
    
    canvas.create_text(canvas.winfo_reqwidth() - 10, 30,
                       text=f"Generations: {generation}", 
                       anchor=tk.NE, fill="green") 
        
    canvas.create_text(canvas.winfo_reqwidth() - 10, canvas.winfo_reqheight() - 10, 
                       text=f"Cost founded : {calculate_distance(current_max_fit.gen):.4f}", 
                       anchor=tk.SE, fill="red")
    
    # root.after(1, create_window)

# Function to update max_fit
def TSPwithGA():
    global start_time
    mutation_rate = 0.1  # Probability of mutation
    population = create_population(CT)
    global current_max_fit
    current_max_fit = individual()
    current_max_fit.gen = population[0].gen
    current_max_fit.fitness = population[0].fitness
    for generation in range(max_generation+1): 
        # new_population = []
        # giữ lại 50% cá thể trội
        half_Size = P_SIZE//2
        # for i in range(half_Size):
        #     new_population.append(population[i])

        # tạo ra 50% cá thể mới
        for i in range(half_Size, P_SIZE-1):

            # tao ra 2 gen moi
            newgen1 = individual()
            newgen1.gen = crossover(population[i].gen, population[i+1].gen)
            newgen1.gen = mutate(newgen1.gen, mutation_rate)
            newgen1.fitness = 1/calculate_distance(newgen1.gen)

            newgen2 = individual()
            newgen2.gen = crossover(population[i].gen, population[i+1].gen)
            newgen2.gen = mutate(newgen2.gen, mutation_rate)
            newgen2.fitness = 1/calculate_distance(newgen2.gen)

            # cho gen moi vào quần thể
            population[i].gen = newgen1.gen
            population[i].fitness = newgen1.fitness
            population[i+1].gen = newgen2.gen
            population[i+1].fitness = newgen2.fitness

        population.sort(reverse=True)
        if current_max_fit.fitness < population[0].fitness:
            current_max_fit.gen = population[0].gen
            current_max_fit.fitness = population[0].fitness

        # Kiểm tra thời gian và thoát khỏi vòng lặp nếu đạt đến 30 giây
        elapsed_time = time.time() - start_time
        if elapsed_time >= 30:
            print("Đã đạt đến thời gian tối đa (30 giây). Dừng thuật toán.")
            break
    return elapsed_time, calculate_distance(current_max_fit.gen), generation
        # Cập nhật canvas        
        # create_window()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("TSP Map")

# Tạo canvas
canvas = tk.Canvas(width=500, height=500)
canvas.pack()

# ct_coord = init_cities_coordinate()
# ct_coord = [City(42, 21), City(53, 64), City(56, 10), City(12, 65), City(23, 64), City(96, 34), City(5, 54), City(20, 36), City(32, 10), City(74, 24)]

def read_file():
    ct_coord = []
    with open("test.txt", "r") as f:
        for line in f:
            x, y = line.split()
            temp = City(float(x), float(y))
            ct_coord.append(temp)
    return ct_coord

ct_coord = init_cities_coordinate()


#doc file

# ct_coord = read_file()
# for i in ct_coord:
#     print(i.x, i.y)



# Gọi hàm TSPwithGA để bắt đầu cập nhật liên tục max_fit
start_time = time.time()  # Lấy thời gian bắt đầu
finish_time, total_distance, generation = TSPwithGA()


# ghi kết quả vào file txt
f = open("ketqua.txt", "a")

# di chuyển con trỏ file đến cuối file
f.write("ket qua lan chay thu:")

# ghi toa do thanh pho
f.write(f"\nSo thanh pho: {CT}")
f.write("\nToa do: ")
for ct in ct_coord:
    f.write(f"({ct.x};{ct.y})")

# ghi thoi gian
f.write(f"\nThoi gian hoan thanh: {finish_time}")

# ghi so luong the he
f.write(f"\nSo luong quan the: {generation}")

# ghi duong di tim duoc
f.write(f"\nduong di: {current_max_fit.gen}")
# ghi ket qua duong di
f.write(f"\nTong duong di: {total_distance}")
f.write("\n")

# Đóng file
f.close()

# Gọi hàm create_window để bắt đầu cập nhật liên tục canvas
create_window()

# Bắt đầu vòng lặp sự kiện Tkinter
root.mainloop()
