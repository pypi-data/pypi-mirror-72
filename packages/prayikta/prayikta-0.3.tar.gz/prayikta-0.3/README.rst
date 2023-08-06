## Prayikta

<p> By using Prayikta module you can  calculate Gaussian distribution, Binomial Probability, pdf and can visualization of them. </p>

### Classes

* Gaussian Class
* Binomial Class
  
#### Gaussian Class

  ```
  # Example Fuctions

    >>> from prayikta import Gaussian
    
    # It has two arguments mean and standard daviation default (mean = 0 and stdev = 1)

    >>> gaussian = Gaussian()
    >>> gaussian.mean
    >>> gaussian.stdev

    # Read data from file and calculate mean and standard deviation

    >>> gaussian.read_data_file('filename.txt')
    >>> gaussian.calculate_mean()
    >>> gaussian.calculate_stdev()
    
    # Plot histogram of data

    >>> gaussian.plot_histogram()

    # Calculate probability density function and visualise it.

    >>> gaussian.pdf() # takes one argument
    >>> gaussian.plot_histogram_pdf()
    

    # Add to gaussian functions

    >>> gaussian_a = Gaussian(25,0)
    >>> gaussian_b = Gaussian(5,2)
    >>> gaussian_c = gaussian_a + gaussian_b
  ```

  #### Binomial Class

  ```
  # Example Fuctions
    >>> from prayikta import Binomial

    # It takes two arguments mean and standard daviation default (probability = 0.5 and size = 20)

    >>> binomial = Binomial()
    >>> binomial.calculate_mean()
    >>> binomial.calculate_stdev()
    
    # Plot bar
    
    >>> binomial.plot_bar()

    # Calculate pdf and visualise it.

    >>> binomial.pdf() # takes one argument
    >>> binomial.plot_bar_pdf()

    # Add to binomial functions

    >>> binomial_a = Binomial(0.5,10)
    >>> binomial_b = Binomial(0.25,20)
    >>> binomial_c = binomial_a + binomial_b
```