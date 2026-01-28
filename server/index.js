import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

import { films } from './film_data.js'
import { directors } from './director_data.js';

const typeDefs = `
    type Query {
        films: [Film!]!
        film(id: ID!): Film!
        directors: [Director!]!
        director(id: ID!): Director!
    }
    type Film {
        id: ID!
        title: String!
        description: String
        releaseDate: String
        director: Director!
        directorId: ID!
    }
    type Director {
        id: ID!
        name: String!
        dob: String
        nationality: String
        films (limit: Int = 3 ): [Film!]!
    }

    type Mutation {
        createDirector(name: String!, dob: String, nationality: String): Director!
        assignFilmToDirector(id: ID!, filmId: ID!): Director!
    }
`;


const resolvers = {
    Query: {
        films: () => films,
        film: (parent, args) => films.find((film) => film.id === args.id),
        directors: () => directors,
        director: (parent, args) => directors.find((director) => director.id === args.id)
    },
    Mutation: {
        createDirector: (parent, args) => {
            const newDirector = {
                id: (directors.length + 1),
                name: args.name,
                dob: args.dob,
                nationality: args.nationality,
                films: []
            };
            directors.push(newDirector);
            return newDirector;
        }
    },
    Film: {
        director: (parent) => directors.find((director) => director.id === parent.directorId)
    },
    Director: {
        films: (parent, args) => {
            console.log(parent)
            return films.filter((film) => film.directorId === parent.id).slice(0, args.limit)
        }
    }
};

const server = new ApolloServer({ typeDefs, resolvers });

const { url } = await startStandaloneServer(server, {
    listen: { port: 4000 },
});

console.log(`🚀  Server ready at ${url}`);