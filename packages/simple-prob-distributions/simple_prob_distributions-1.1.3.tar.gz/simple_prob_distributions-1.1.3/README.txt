# How to Install 
1. install using pip. Enter 'pip install simple_prob_distributions'

## Package Includes
### Normal (Gaussian) Distribution
  - Gaussian Distribution, is the normal bell-shaped distribution implemented in Gaussian  class.
    
    <b> How to use </b>
    from simple_prob_distributions import Gaussian
    
    gaussian = Gaussian(mean_value, standard_deivation_value)
    
    <b> Attributes </b>
    mean: mean of the data (mu) 
    stdev: standard deviation of the data (sigma)
    data: sample data
    
    <b> Methods </b>
    calculate_mean()
    calculate_stdev()
    plot_histogram()
    plot_histogram_pdf()
    pdf(x)
    
    <b> Magic Methods </b>
    __add__
    __repr__

## Binomial Distribution
  - Gaussian Distribution, is the normal bell-shaped distribution implemented in Gaussian  class.
    
    <b> How to use </b>
    from simple_prob_distributions import Gaussian
    
    gaussian = Gaussian(mean_value, standard_deivation_value)
    
    <b> Attributes </b>
    p: success probability
    n: number of samples
    data: sample data
    mean: mean of the data (mu) 
    stdev: standard deviation of the sdata (sigma)
    
    <b> Methods </b>
    calculate_mean()
    calculate_stdev()
    replace_stats_with_data()
    plot_bar()
    plot_bar_pdf()
    pdf(k)
    
    <b> Magic Methods </b>
    __add__
    __repr__