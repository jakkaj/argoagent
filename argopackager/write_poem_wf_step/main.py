
import os

import openai
import sys
def main():   
    name = "Write Poem"
    # open /tmp/input.txt and read the first line
    input_var = """

Title: Pluto Summary: Pluto (minor-planet designation: 134340 Pluto) is a dwarf planet in the Kuiper belt, a ring of bodies beyond the orbit of Neptune. It is the ninth-largest and tenth-most-massive known object to directly orbit the Sun. It is the largest known trans-Neptunian object by volume by a small margin, but is less massive than Eris. Like other Kuiper belt objects, Pluto is made primarily of ice and rock and is much smaller than the inner planets. Pluto has roughly one-sixth the mass of the Moon, and one-third its volume. Originally considered a planet, its status was changed when a new definition of the word was adopted by astronomers. Pluto has a moderately eccentric and inclined orbit, ranging from 30 to 49 astronomical units (4.5 to 7.3 billion kilometres; 2.8 to 4.6 billion miles) from the Sun. Light from the Sun takes 5.5 hours to reach Pluto at its orbital distance of 39.5 AU (5.91 billion km; 3.67 billion mi). Pluto's eccentric orbit periodically brings it closer to the Sun than Neptune, but a stable orbital resonance prevents them from colliding. Pluto has five known moons: Charon, the largest, whose diameter is just over half that of Pluto; Styx; Nix; Kerberos; and Hydra. Pluto and Charon are sometimes considered a binary system because the barycenter of their orbits does not lie within either body, and they are tidally locked. New Horizons was the first spacecraft to visit Pluto and its moons, making a flyby on July 14, 2015, and taking detailed measurements and observations. Pluto was discovered in 1930 by Clyde W. Tombaugh, making it the first known object in the Kuiper belt. It was immediately hailed as the ninth planet. However,: 27  its planetary status was questioned when it was found to be much smaller than expected. These doubts increased following the discovery of additional objects in the Kuiper belt starting in the 1990s, particularly the more massive scattered disk object Eris in 2005. In 2006, the International Astronomical Union (IAU) formally redefined the term planet to exclude dwarf planets such as Pluto. Many planetary astronomers, however, continue to consider Pluto and other dwarf planets to be planets.
    """
   
    

    #input_var = "no var detected"
    if len(sys.argv) == 2:
        input_var = sys.argv[1]

    
    
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not openai.api_key:
        print("OPENAI_API_KEY not found in environment variables.")
        return

    try:
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", 
                 "content": f"Write a poem about the follow information: {input_var}"}
            ]
        )
        summary = completion.choices[0].message.content
        print(summary)

        output_file = f"/tmp/output.txt"
        with open(output_file, "w") as f:
            f.write(summary)

    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return

if __name__ == "__main__":
    main()
