import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    "*** YOUR CODE HERE ***"

    domain_file.write("Propositions:\n")
    for peg in pegs:
        domain_file.write(peg + "_empty ")

    for i in range(n_):
        for j in range(n_):
            if i < j:
                domain_file.write(disks[i] + "_on_" + disks[j] + " ")
    for disk in disks:
        for peg in pegs:
            domain_file.write(disk + "_in_" + peg + " ")

    for disk in disks:
            domain_file.write(disk + "_low ")
            domain_file.write(disk + "_high ")

    domain_file.write("\nActions:")

    for i in range(n_):
        for j in range(m_):
            for k in range(m_):
                if j != k:
                    for bigger_disk in range(i+1,n_):
                        for bigger_disk_2 in range(i + 1,n_):
                            if bigger_disk != bigger_disk_2:
                                name = "\nName: move_" + disks[i] +"_in_" +pegs[j] +"_on_"+disks[bigger_disk]+ "_to_" +pegs[k]+"_on_"+disks[bigger_disk_2]

                                pre = "\npre: " + disks[i] + "_in_" + pegs[j]
                                pre += " " + disks[i] + "_high"
                                pre += " " + disks[i] + "_on_" + disks[bigger_disk]
                                pre += " " +disks[bigger_disk_2] +"_in_" + pegs[k]
                                pre += " " + disks[bigger_disk_2] + "_high"

                                add = "\nadd: " + disks[i] + "_in_" + pegs[k]
                                add += " " +  disks[i] + "_on_" + disks[bigger_disk_2]
                                add += " " + disks[bigger_disk] + "_high"

                                dele = "\ndel: " + disks[i] + "_in_" + pegs[j]
                                dele += " " + disks[i] + "_on_" + disks[bigger_disk]
                                dele += " " + disks[bigger_disk_2] + "_high"

                                domain_file.write(name + pre + add + dele)

    for i in range(n_):
        for j in range(m_):
            for k in range(m_):
                if j != k:
                    for bigger_disk in range(i+1,n_):
                        name = "\nName: move_" + disks[i] +"_in_" +pegs[j] +"_to_"+  pegs[k] + "_on_" +disks[bigger_disk]

                        pre = "\npre: " + disks[i] + "_in_" + pegs[j]
                        pre += " " + disks[i] + "_high"
                        pre += " " + disks[i] + "_low"
                        pre += " " + disks[bigger_disk] + "_in_" + pegs[k]
                        pre += " " + disks[bigger_disk] + "_high"

                        add = "\nadd: " + disks[i] + "_in_" + pegs[k]
                        add += " " + disks[i] + "_on_" +disks[bigger_disk]
                        add += " " + pegs[j] + "_empty"

                        dele = "\ndel: " + disks[i] + "_in_" + pegs[j]
                        dele += " " + disks[i] + "_low"
                        dele += " " + disks[bigger_disk] + "_high"

                        domain_file.write(name + pre + add + dele)

    for i in range(n_):
        for j in range(m_):
            for k in range(m_):
                if j != k:
                    name = "\nName: move_" + disks[i] +"_in_" +pegs[j] +"_to_"+ pegs[k]

                    pre = "\npre: " + disks[i] + "_in_" + pegs[j]
                    pre += " " + disks[i] + "_high"
                    pre += " " + disks[i] + "_low"
                    pre +=" "+ pegs[k] + "_empty"

                    add = "\nadd: " + disks[i] + "_in_" + pegs[k]
                    add += " " + pegs[j] + "_empty"

                    dele = "\ndel: " + disks[i] + "_in_" + pegs[j]
                    dele += " " + pegs[k] + "_empty"

                    domain_file.write(name + pre + add + dele)

    for i in range(n_):
        for j in range(m_):
            for k in range(m_):
                if j != k:
                    for bigger_disk in range(i+1,n_):
                        name = "\nName: move_" + disks[i] +"_in_" + pegs[j] +"_on_" + disks[bigger_disk]+ "_to_"+ pegs[k]

                        pre = "\npre: " + disks[i] + "_in_" + pegs[j]
                        pre += " " + disks[i] + "_high"
                        pre += " " + disks[i] +"_on_"+ disks[bigger_disk]
                        pre += " " + pegs[k] + "_empty"

                        add = "\nadd: " + disks[i] + "_in_" + pegs[k]
                        add += " " + disks[i] + "_low"
                        add += " " + disks[bigger_disk] + "_high"

                        dele = "\ndel: " + disks[i] + "_in_" + pegs[j]
                        dele += " " + disks[i] +"_on_"+ disks[bigger_disk]
                        dele += " " + pegs[k] + "_empty"

                        domain_file.write(name + pre + add + dele)

    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    "*** YOUR CODE HERE ***"

    problem_file.write("Initial state: ")
    for i in range(n_):
        for j in range(n_):
            if i == j-1:
                problem_file.write(disks[i] + "_on_" + disks[j] + " ")

    for disk in disks:
        problem_file.write(disk + "_in_" + pegs[0] + " ")

    problem_file.write(disks[0] + "_high ")
    problem_file.write(disks[n_-1] + "_low ")

    for peg in pegs:
        if peg != pegs[0]:
            problem_file.write(peg + "_empty ")

    problem_file.write("\nGoal state: ")
    for disk in disks:
        problem_file.write(disk + "_in_" + pegs[m_-1] + " ")

    for i in range(n_):
        for j in range(n_):
            if i == j-1:
                problem_file.write(disks[i] + "_on_" + disks[j] + " ")

    problem_file.write(disks[0] + "_high ")
    problem_file.write(disks[n_-1] + "_low ")

    for peg in pegs:
        if peg != pegs[m_-1]:
            problem_file.write(peg + "_empty ")

    problem_file.close()




if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
