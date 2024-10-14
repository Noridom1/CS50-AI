from heredity import joint_probability
people = {'Lily': {"mother": None, "father": None},
          'James': {"mother": None, "father": None},
          'Harry': {"mother": "Lily", "father": "James"}}
one_gene = {}
two_genes = {'Harry','Lily', "James"}
have_trait = {'Harry','Lily', "James"}
p = joint_probability(people, one_gene, two_genes, have_trait)
print(p)
# Result should be = 0.0026643247488s
