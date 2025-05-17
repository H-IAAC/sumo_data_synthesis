import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from pprint import pprint

def parseVehicleDistributionsXML(param_dict, vtypes_dist, styles, root_folder, car_follow_model="IDM", lc_model="SL2015"):
    xml = "<root>\n"
    for style in styles:
        xml += f'<vTypeDistribution id=\"{style}\">\n'

        for vtype in vtypes_dist[f'veh_{style}']:
            xml += f'\t<vType id=\"{vtype}\" carFollowModel=\"{car_follow_model}\" laneChangeModel=\"{lc_model}\" '

            for parameter in param_dict.keys():
                xml += f"{parameter}=\"{vtypes_dist['veh_{}'.format(style)][vtype][parameter]}\" "

            xml += f"probability=\"{vtypes_dist['veh_{}'.format(style)][vtype]['probability']}\">\n"
            xml += '\t\t<param key="device.rerouting.probability" value="1.0"/>\n'
            xml += '\t\t<param key="device.rerouting.adaptation-steps" value="18"/>\n'
            xml += '\t\t<param key="device.rerouting.adaptation-interval" value="10"/>\n'
            xml += '\t</vType>\n'

        xml += "</vTypeDistribution>\n"
    
    xml += "</root>\n"

    with open (f"{root_folder}/vTypesDistribution.xml", "w") as f:
        f.write(xml)
    return xml

def parseVehicleTypesXML(param_dict, styles, root_folder, car_follow_model="IDM", lc_model="SL2015"):
    xml = "<root>\n"
    for style in styles:

        xml += f'<vType id=\"{style}\" carFollowModel=\"{car_follow_model}\" laneChangeModel=\"{lc_model}\" '
        for parameter, value in param_dict.items():
            xml += f"{parameter}='{value[style]}' "
        xml += ">\n"
        xml += '\t<param key="device.rerouting.probability" value="1.0"/>\n'
        xml += '\t<param key="device.rerouting.adaptation-steps" value="18"/>\n'
        xml += '\t<param key="device.rerouting.adaptation-interval" value="10"/>\n'
        xml += '</vType>\n'

    xml += "</root>\n"
    with open (f"{root_folder}/vTypesDistribution.xml", "w") as f:
        f.write(xml)
    return xml

def generateVehicleTypesLLM(param_dict, styles, n):
    # This function generates n vehicle types for each style in the styles list based on the given distribution and assigns a probability to each vType based on how likely it is to be real
    # n is the number of vTypes for each vTypeDistribution
    # styles is the list of styles to be generated (agg, norm, for example)
    vtypes_dist = {}
    param_probs = np.zeros(n) # Keeps the probability score for each of the generated vTypes
    for style in styles:
        vtypes_dist[f'veh_{style}'] = {}
        for i in range(n):
            vtypes_dist[f'veh_{style}'][f'v_{style}{i}'] = {}
            prob = 0
            for parameter in list(param_dict.keys()):
                value, probability = getParamValueLLM(param_dict, parameter, style) # Gets value for parameter and the probability of getting that value
                vtypes_dist[f'veh_{style}'][f'v_{style}{i}'][parameter] = float(value)
                prob += probability # Sum of probabilities for each parameter
    
            param_probs[i] = prob

        softm = np.exp(param_probs) / np.sum(np.exp(param_probs)) # Softmax function to normalize the probabilities

        for i in range(n):
            vtypes_dist[f'veh_{style}'][f'v_{style}{i}']["probability"] = softm[i] # Assigning the normalized probability to each vType

    return vtypes_dist

def getParamValueLLM(param_dict, parameter, style):
    
    m = (param_dict[parameter][style]['min'] + param_dict[parameter][style]['max'])/2
    s = (param_dict[parameter][style]['max'] - m) / stats.norm.ppf(0.975) # Finding the standard deviation for 95% of the data to be within the range
    value = np.round(np.random.normal(m, s), 2)
    
    if s <= 0:
        print(f"Error: The standard deviation for {parameter} is {s}")

    cdf = stats.norm.cdf(value, loc=m, scale=s)
    if value > m:
        probability = 1 - cdf
    else:
        probability = cdf
        
    return value, probability


def showGaussianLLM(param_dict, parameters, styles):
    num_params = len(parameters)
    num_rows = (num_params + 1) // 2
    fig, axes = plt.subplots(num_rows, 2, figsize=(14, 6 * num_rows))

    axes = axes.flatten()

    for ax, parameter in zip(axes, parameters):
        for style in styles:
            m = (param_dict[parameter][style]['min'] + param_dict[parameter][style]['max']) / 2
            s = (param_dict[parameter][style]['max'] - m) / stats.norm.ppf(0.975)  # Finding the standard deviation for 95% of the data to be within the range

            # Generate data
            data = np.random.normal(m, s, 5000)

            # Plot the data
            ax.hist(data, bins=30, density=True, alpha=0.6, label=f'{style} style')

            # Plot the Gaussian distribution
            xmin, xmax = ax.get_xlim()
            x = np.linspace(xmin, xmax, 100)
            p = np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))
            ax.plot(x, p, linewidth=2)

        ax.set_title(f'Gaussian Distribution for {parameter}')
        ax.legend()

    # Hide any unused subplots
    for i in range(len(parameters), len(axes)):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.show()