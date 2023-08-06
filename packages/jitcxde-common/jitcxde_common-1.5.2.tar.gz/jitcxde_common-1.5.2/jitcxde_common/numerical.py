import numpy as np

def random_direction(n):
	"""
	returns an n-dimensional vector with random direction and length n
	"""
	vector = np.random.normal(0,1,n)
	return vector/np.linalg.norm(vector)

def orthonormalise(vectors):
	"""
	Orthonormalise vectors in place (with Gram-Schmidt) and return their norms after orthogonalisation (but before normalisation).
	"""
	norms = []
	for i,vector in enumerate(vectors):
		for j in range(i):
			vector -= np.dot( vector, vectors[j] ) * vectors[j]
		norm = np.linalg.norm(vector)
		vector /= norm
		norms.append(norm)
	
	return np.array(norms)

def rel_dist(x,y):
	x = np.asarray(x)
	y = np.asarray(y)
	return np.linalg.norm(x-y)/np.linalg.norm(np.mean((x,y)))

