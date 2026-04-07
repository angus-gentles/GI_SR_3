#!/usr/bin/env bash

run_them_2 () { 
    cur=$(pwd)
    x=$1
    y=$2
    N=2
    x1=$(echo "print(1-$x)" | python3)
    y1=$(echo "print(1-$y)" | python3)
    name=In${x}Ga${x1}As${y1}Sb${y}_cube_${N}x${N}x${N}
    mkdir dir_${name}
    cd dir_${name}
    #first_process.py -x $x -y $y -N $N $N $N --yamlbase ../cube_2.yaml --base ${name}
    cp ../ksection*.txt .
    cp ../*.json .
    write_Uin.py -x $x -y $y -N $N $N $N --base ${name}

    quantum_espresso_first_step.py -x $x -y $y -N $N $N $N \
     --yamlresult ${name}.result.yaml  \
     --crysresult ${name}.crys --nbnd 56 \
     --base ${name} --ksection ../ksection_relax.txt

    #srun -n ${SLURM_NPROCS} pw.x -i ${name}.relax.in > ${name}.relax.out

    #relax_crys.py -x $x -y $y -N $N $N $N --relaxout ${name}.relax.out --crysout ${name}.out.crys

	#quantum_espresso_scf.py -x $x -y $y -N $N $N $N --crysout ${name}.out.crys --nbnd 56 --ksection ../ksection_scf.txt --base ${name}
	
    #srun -n ${SLURM_NPROCS} pw.x -i ${name}.scf.in > ${name}.scf.out

	#remove_wfc.sh

    cd ${cur}
 }
 
run_them () { 
    cur=$(pwd)
    x=$1
    y=$2
    N=$3
    x1=$(echo "print(1-$x)" | python3)
    y1=$(echo "print(1-$y)" | python3)
    name=In${x}Ga${x1}As${y1}Sb${y}_cube_${N}x${N}x${N}
    mkdir -p dir_${name}
    cd dir_${name}
    cur1=$(pwd)

    write_Uin.py -x $x -y $y -N $N $N $N --base ${name} --Ubase ../U_base.json

    make_crys.py -ba ${name} -bc ../base.cube_${N}x${N}x${N}.crys -sl B -ol In

    for file in ${name}.*.crys; do
    echo $file
        i=$(echo "$file" | sed -n "s/.*_cube_3x3x3\.\([0-9]*\)\.crys/\1/p")
        echo $i
        mkdir -p "calc_$i"
        mv ${name}.${i}.crys calc_$i/
    done

    echo $i

    for j in $(seq 0 $i) ; do
        cd calc_$j
        quantum_espresso_first_step.py -x $x -y $y -N $N $N $N \
         --yamlresult ${name}.result.yaml  \
         --crysresult ${name}.crys --nbnd 56 \
         --base ${name}.${j} --ksection ../../ksection_relax.txt \
         --U_file ../${name}.U_in.json --crysresult ${name}.${j}.crys\
         --input_data ../../input_data.json --pseudopotentials ../../pseudopotentials.json --lattice_constant_file ../../a_base.json

        srun -n ${SLURM_NPROCS} pw.x -i ${name}.${j}.relax.in > ${name}.${j}.relax.out 

        relax_crys.py -x $x -y $y -N $N $N $N --relaxout ${name}.$j.relax.out --crysout ${name}.$j.out.crys

        quantum_espresso_scf.py -x $x -y $y -N $N $N $N --crysout ${name}.${j}.out.crys \
                                --nbnd 56 --ksection ../../ksection_scf.txt --base ${name}.$j \
                                --input_data ../../input_data.json --pseudopotentials ../../pseudopotentials.json \
                                --U_file ../${name}.U_in.json 

        srun -n ${SLURM_NPROCS} pw.x -i ${name}.${j}.scf.in > ${name}.${j}.scf.out

        remove_wfc.sh

        cd $cur1
    done

    cd ${cur}
 }

run_them_cont () { 
    cur=$(pwd)
    x=$1
    y=$2
    N=$3
    x1=$(echo "print(1-$x)" | python3)
    y1=$(echo "print(1-$y)" | python3)
    name=In${x}Ga${x1}As${y1}Sb${y}_cube_${N}x${N}x${N}
    mkdir -p dir_${name}
    cd dir_${name}
    cur1=$(pwd)

    for j in $(seq 0 9); do
        cd calc_$j
        ls
        
        relax_done=false
        for f in *.relax.out; do
            [[ -e "$f" ]] || continue  # skip if no .scf.out files exist
            #if grep -q "DONE" "$f"; then
                relax_done=true
                break
            #fi
        done
        
        # Check if any *.scf.out file contains 'DONE'
        scf_done=false
        for f in *.scf.out; do
            [[ -e "$f" ]] || continue  # skip if no .scf.out files exist
            #if grep -q "DONE" "$f"; then
                scf_done=true
                break
            #fi
        done

        if [[ "$relax_done" == false ]]; then
            echo "going relax $j"
            
            quantum_espresso_first_step.py -x $x -y $y -N $N $N $N \
            --yamlresult ${name}.result.yaml  \
            --crysresult ${name}.crys --nbnd 56 \
            --base ${name}.${j} --ksection ../../ksection_relax.txt \
            --U_file ../${name}.U_in.json --crysresult ${name}.${j}.crys \
            --input_data ../../input_data.json --pseudopotentials ../../pseudopotentials.json --lattice_constant_file ../../a_base.json

            srun -n ${SLURM_NPROCS} pw.x -i ${name}.${j}.relax.in > ${name}.${j}.relax.out 
        else
            echo "Skipping Relaxation calc_$j: Relaxation already completed."
        fi

        if [[ "$scf_done" == false ]]; then
            relax_crys.py -x $x -y $y -N $N $N $N --relaxout ${name}.$j.relax.out --crysout ${name}.$j.out.crys

            quantum_espresso_scf.py -x $x -y $y -N $N $N $N --crysout ${name}.${j}.out.crys \
                                    --nbnd 56 --ksection ../../ksection_scf.txt --base ${name}.$j \
                                    --input_data ../../input_data.json --pseudopotentials ../../pseudopotentials.json \
                                    --U_file ../${name}.U_in.json 

            srun -n ${SLURM_NPROCS} pw.x -i ${name}.${j}.scf.in > ${name}.${j}.scf.out

            remove_wfc.sh
            
        else
            echo "Skipping calc_$j: SCF already completed."
        fi

        cd "$cur1"
    done

    cd ${cur}
 }
 
run_them_scf () { 
    cur=$(pwd)
    x=$1
    y=$2
    N=$3
    x1=$(echo "print(1-$x)" | python3)
    y1=$(echo "print(1-$y)" | python3)
    name=In${x}Ga${x1}As${y1}Sb${y}_cube_${N}x${N}x${N}
    #mkdir dir_${name}
    cd dir_${name}
    cur1=$(pwd)

    i=9

    for j in $(seq 0 $i); do
        cd calc_$j

        relax_file="${name}.$j.relax.out"
        scf_file="${name}.$j.scf.out"

        if grep -q "DONE" "$relax_file" && ! grep -q "DONE" "$scf_file"; then
            pwd
            #relax_crys.py -x $x -y $y -N $N $N $N \
            #            --relaxout "$relax_file" \
            #            --crysout "${name}.$j.out.crys"

            quantum_espresso_scf.py -x $x -y $y -N $N $N $N \
                                    --crysout "${name}.${j}.out.crys" \
                                    --nbnd 56 \
                                    --ksection ../../ksection_scf.txt \
                                    --base "${name}.$j" \
                                    --input_data ../../input_data.json \
                                    --pseudopotentials ../../pseudopotentials.json \
                                    --U_file ../${name}.U_in.json 

            srun -n ${SLURM_NPROCS} pw.x -i "${name}.${j}.scf.in" > "$scf_file"

            remove_wfc.sh

        else
            echo "Skipping calc_$j: relax not done or scf already done."
        fi

        cd "$cur1"
    done

    cd ${cur}
 }
